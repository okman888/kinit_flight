#!/usr/bin/python
# -*- coding: utf-8 -*-

import asyncio
import json
import random
import re
import uuid
from datetime import datetime, timedelta

from application.settings import FLIGHT_TASK_REQUEST_INTERVAL_MAX, FLIGHT_TASK_REQUEST_INTERVAL_MIN
from core.database import session_factory
from core.logger import logger
from utils.excel.excel_manage import ExcelManage
from . import models, crud
from .providers import flight_provider_registry


def _task_done_callback(async_task: asyncio.Task):
    if async_task.cancelled():
        return
    exc = async_task.exception()
    if exc:
        logger.exception(f"flight task execute failed: {str(exc)}")


def submit_flight_task(
        task_id: str,
        account: str | None = None,
        password: str | None = None,
        http_proxy: str | None = None,
        https_proxy: str | None = None,
        retry_failed_only: bool = False
) -> None:
    # 脱离请求生命周期执行，避免请求线程长期占用
    async_task = asyncio.create_task(
        run_flight_task(task_id, account, password, http_proxy, https_proxy, retry_failed_only)
    )
    async_task.add_done_callback(_task_done_callback)


def _date_range(start_date: str, end_date: str) -> list[datetime]:
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    if end < start:
        raise ValueError("结束日期不能早于开始日期")
    result = []
    current = start
    while current <= end:
        result.append(current)
        current += timedelta(days=1)
    return result


def _safe_int(value) -> int | None:
    if value in [None, ""]:
        return None
    try:
        return int(float(value))
    except Exception:
        return None


def _fmt_ods_create_time(value: datetime) -> str:
    text = value.strftime("%d/%m/%Y %H:%M:%S.%f")
    return text[:-3]


def _fmt_ods_date(value: datetime) -> str:
    return value.strftime("%d/%m/%Y 00:00:00")


def _parse_dt_text(value: str | None) -> str | None:
    if not value:
        return None
    for fmt in ["%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S"]:
        try:
            return datetime.strptime(value, fmt).strftime("%Y-%m-%d %H:%M:%S")
        except ValueError:
            continue
    return value


def _request_key(departure_city: str, arrival_city: str, travel_date: datetime) -> str:
    return f"{departure_city.upper()}|{arrival_city.upper()}|{travel_date.strftime('%Y-%m-%d')}"


def _extract_retry_count(message: str) -> int:
    match = re.search(r"retry=(\d+)", message or "")
    if match:
        return max(int(match.group(1)) - 1, 0)
    match = re.search(r"已重试(\d+)次", message or "")
    if match:
        return max(int(match.group(1)), 0)
    return 0


def _random_interval() -> float:
    return random.uniform(FLIGHT_TASK_REQUEST_INTERVAL_MIN, FLIGHT_TASK_REQUEST_INTERVAL_MAX)


def _expand_task_requests(items: list[dict]) -> list[dict]:
    requests: list[dict] = []
    for item in items:
        for travel_date in _date_range(item["start_date"], item["end_date"]):
            requests.append({
                "departure_city": item.get("departure_city", "").upper(),
                "departure_city_name": item.get("departure_city_name"),
                "arrival_city": item.get("arrival_city", "").upper(),
                "arrival_city_name": item.get("arrival_city_name"),
                "travel_date": travel_date,
            })
    return requests


def _pick_failed_requests_only(expected_requests: list[dict], logs: list[models.FlightTaskLog]) -> list[dict]:
    latest_status: dict[str, str] = {}
    for log in logs:
        key = _request_key(log.departure_city, log.arrival_city, log.travel_date)
        if key not in latest_status:
            latest_status[key] = log.status
    failed_requests: list[dict] = []
    for request in expected_requests:
        key = _request_key(request["departure_city"], request["arrival_city"], request["travel_date"])
        if latest_status.get(key) == "failed":
            failed_requests.append(request)
    return failed_requests


def _calc_task_progress(expected_requests: list[dict], logs: list[models.FlightTaskLog]) -> tuple[int, int]:
    latest_status: dict[str, str] = {}
    for log in logs:
        key = _request_key(log.departure_city, log.arrival_city, log.travel_date)
        if key not in latest_status:
            latest_status[key] = log.status
    failed = 0
    for request in expected_requests:
        key = _request_key(request["departure_city"], request["arrival_city"], request["travel_date"])
        if latest_status.get(key) != "success":
            failed += 1
    success = len(expected_requests) - failed
    return success, failed


def _convert_rows(task_db_id: int, task_public_id: str, item: dict, travel_date: datetime, channel: str, flights: list) -> list[dict]:
    rows = []
    now = datetime.now()
    for flight in flights:
        segs = flight.get("fromsegs", []) or []
        first_seg = segs[0] if segs else {}
        last_seg = segs[-1] if segs else {}
        layovers = [seg.get("arr", "") for seg in segs[:-1] if seg.get("arr")]
        default_cabin = ",".join([seg.get("cabinclass", "") for seg in segs if seg.get("cabinclass")])
        flights_info = ",".join([f"{seg.get('dept', '')}:{seg.get('flightno', '')}" for seg in segs if seg.get("flightno")])
        if flights_info:
            flights_info = flights_info + ","
        rows.append({
            "task_db_id": task_db_id,
            "task_id": task_public_id,
            "create_time": _fmt_ods_create_time(now),
            "row_id": str(uuid.uuid4().int)[:19],
            "travel_date": travel_date,
            "departure_city": item.get("departure_city", "").upper(),
            "departure_city_name": item.get("departure_city_name"),
            "departure_time": _parse_dt_text(first_seg.get("depttime")),
            "arrival_city": item.get("arrival_city", "").upper(),
            "arrival_city_name": item.get("arrival_city_name"),
            "arrival_time": _parse_dt_text(last_seg.get("arrtime")),
            "duration": sum([_safe_int(seg.get("flighttime")) or 0 for seg in segs]) if segs else None,
            "stopover": ",".join(layovers) + ("," if layovers else ""),
            "stopover_duration": None,
            "min_price": _safe_int(flight.get("adult_price")),
            "min_price_tax": _safe_int(flight.get("adult_tax")),
            "min_price_discount": None,
            "min_business_price": None,
            "min_business_price_tax": None,
            "departure_airport": first_seg.get("dept"),
            "departure_airport_name": None,
            "departure_terminal": first_seg.get("depttrmn"),
            "arrival_airport": last_seg.get("arr"),
            "arrival_airport_name": None,
            "arrival_terminal": last_seg.get("arrtrmn"),
            "seat_left": str(flight.get("seatcount")) if flight.get("seatcount") is not None else None,
            "default_cabin": default_cabin or None,
            "segment_list": json.dumps(segs, ensure_ascii=False),
            "economy_policies": None,
            "business_policies": None,
            "flights_info": flights_info,
            "data_source": channel,
            "raw_payload": json.dumps(flight, ensure_ascii=False)
        })
    return rows


async def export_task_to_excel(task_id: str) -> dict | None:
    async with session_factory() as db:
        task: models.FlightTask | None = await crud.FlightTaskDal(db).get_data(task_id=task_id, v_return_none=True)
        if not task:
            return None
        itineraries = await crud.FlightItineraryDal(db).get_datas(limit=0, task_id=task_id, v_return_objs=True)
        headers = [
            "create_time", "id", "travel_date", "departure_city", "departure_city_name",
            "departure_time", "arrival_city", "arrival_city_name", "arrival_time", "duration",
            "stopover", "stopover_duration", "min_price", "min_price_tax", "min_price_discount",
            "min_business_price", "min_business_price_tax", "departure_airport", "departure_airport_name",
            "departure_terminal", "arrival_airport", "arrival_airport_name", "arrival_terminal",
            "seat_left", "default_cabin", "segment_list", "economy_policies", "business_policies",
            "flights_info", "data_source", "task_id"
        ]
        rows = []
        for item in itineraries:
            rows.append([
                item.create_time,
                item.row_id,
                _fmt_ods_date(item.travel_date),
                item.departure_city,
                item.departure_city_name,
                item.departure_time,
                item.arrival_city,
                item.arrival_city_name,
                item.arrival_time,
                item.duration,
                item.stopover,
                item.stopover_duration,
                item.min_price,
                item.min_price_tax,
                item.min_price_discount,
                item.min_business_price,
                item.min_business_price_tax,
                item.departure_airport,
                item.departure_airport_name,
                item.departure_terminal,
                item.arrival_airport,
                item.arrival_airport_name,
                item.arrival_terminal,
                item.seat_left,
                item.default_cabin,
                item.segment_list,
                item.economy_policies,
                item.business_policies,
                item.flights_info,
                item.data_source,
                item.task_id
            ])
        em = ExcelManage()
        em.create_excel("ods_itinerary")
        em.write_list(rows, headers)
        remote_file_url = em.save_excel(path="flight_itinerary").get("remote_path")
        em.close()
        task.result_file_url = remote_file_url
        await db.commit()
        return {"url": remote_file_url, "filename": f"{task_id}.xlsx"}


async def run_flight_task(
        task_id: str,
        account: str | None = None,
        password: str | None = None,
        http_proxy: str | None = None,
        https_proxy: str | None = None,
        retry_failed_only: bool = False
) -> None:
    async with session_factory() as db:
        task: models.FlightTask | None = await crud.FlightTaskDal(db).get_data(task_id=task_id, v_return_none=True)
        if not task:
            return
        try:
            payload = json.loads(task.task_payload)
            channel = payload.get("channel", "hk.trip.com")
            provider = flight_provider_registry.get(channel)
            account = account or provider.default_account
            password = password or provider.default_password
            items = payload.get("items", [])
            expected_requests = _expand_task_requests(items)
            task_db_id = task.id
            task_public_id = task.task_id
            task_log_enabled = True
            total_days = 0
            total_requests = 0
            for item in items:
                days = len(_date_range(item["start_date"], item["end_date"]))
                total_days += days
                total_requests += days

            current_requests = expected_requests
            task_logs = []
            try:
                task_logs = await crud.FlightTaskLogDal(db).get_datas(
                    limit=0,
                    task_id=task_id,
                    v_return_objs=True,
                    v_order="desc",
                    v_order_field="create_datetime"
                )
            except Exception as log_error:
                task_log_enabled = False
                logger.warning(f"flight_task_log unavailable, fallback mode enabled: {str(log_error)}")

            if retry_failed_only:
                if not task_log_enabled:
                    raise ValueError("缺少 flight_task_log 表，无法仅重试失败请求，请先迁移数据库")
                current_requests = _pick_failed_requests_only(expected_requests, task_logs)

            task.status = "collecting"
            task.message = "任务采集中"
            task.started_at = datetime.now()
            task.total_routes = len(items)
            task.total_days = total_days
            task.total_requests = total_requests
            if not retry_failed_only:
                task.success_requests = 0
                task.failed_requests = 0
                task.result_count = 0
                task.result_file_url = None
            await db.commit()

            if retry_failed_only and len(current_requests) == 0:
                task.status = "completed"
                task.finished_at = datetime.now()
                task.message = "任务采集完成，无失败请求可重试"
                await db.commit()
                return

            run_success_requests = 0
            run_failed_requests = 0
            errors = []
            request_count = len(current_requests)
            for idx, request_item in enumerate(current_requests):
                travel_date = request_item["travel_date"]
                run_started = datetime.now()
                query_payload = provider.build_query_payload(request_item, travel_date)
                ok, message, flights = await provider.query_flights(
                    query_payload,
                    account,
                    password,
                    http_proxy,
                    https_proxy
                )
                execute_ms = int((datetime.now() - run_started).total_seconds() * 1000)

                if task_log_enabled:
                    await crud.FlightTaskLogDal(db).create_data(
                        data={
                            "task_db_id": task_db_id,
                            "task_id": task_public_id,
                            "departure_city": request_item["departure_city"],
                            "arrival_city": request_item["arrival_city"],
                            "travel_date": travel_date,
                            "status": "success" if ok else "failed",
                            "execute_ms": execute_ms,
                            "retry_count": _extract_retry_count(message),
                            "message": message,
                            "create_datetime": datetime.now()
                        }
                    )

                if not ok:
                    run_failed_requests += 1
                    errors.append(
                        f"{request_item.get('departure_city')}-{request_item.get('arrival_city')} "
                        f"{travel_date.strftime('%Y-%m-%d')} {message}"
                    )
                    await db.commit()
                else:
                    rows = _convert_rows(task_db_id, task_public_id, request_item, travel_date, channel, flights)
                    if rows:
                        await crud.FlightItineraryDal(db).create_datas(rows)
                    run_success_requests += 1
                    await db.commit()

                if idx < request_count - 1:
                    interval = _random_interval()
                    logger.info(f"请求间隔等待 {interval:.2f} 秒")
                    await asyncio.sleep(interval)

            await export_task_to_excel(task_id)
            if task_log_enabled:
                all_logs = await crud.FlightTaskLogDal(db).get_datas(
                    limit=0,
                    task_id=task_id,
                    v_return_objs=True,
                    v_order="desc",
                    v_order_field="create_datetime"
                )
                success_requests, failed_requests = _calc_task_progress(expected_requests, all_logs)
            else:
                success_requests = run_success_requests
                failed_requests = run_failed_requests
            task.success_requests = success_requests
            task.failed_requests = failed_requests
            task.result_count = await crud.FlightItineraryDal(db).get_count(task_id=task_id)
            task.finished_at = datetime.now()
            task.status = "completed"
            if failed_requests == 0:
                task.message = "任务采集完成"
            elif success_requests > 0:
                task.message = "任务采集完成，部分请求失败"
            else:
                task.message = "任务采集完成，但全部请求失败"
            if errors:
                task.message = f"{task.message}；错误数：{len(errors)}"
            await db.commit()
        except Exception as e:
            logger.exception(f"run_flight_task failed, task_id={task_id}")
            task.status = "failed"
            task.finished_at = datetime.now()
            task.message = f"任务执行异常：{str(e)}"
            await db.commit()
