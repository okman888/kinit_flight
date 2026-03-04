#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import annotations

import asyncio
import importlib.util
import os
import sys
from datetime import datetime
from pathlib import Path

from application.settings import BASE_DIR

from .base import FlightProvider

REQUEST_MAX_RETRIES = 3
RETRY_SLEEP_SECONDS = 2


class TripProvider(FlightProvider):
    _trip_module = None

    @property
    def channel(self) -> str:
        return "hk.trip.com"

    @property
    def default_account(self) -> str | None:
        return os.getenv("TRIP_ACCOUNT", "727735746@qq.com")

    @property
    def default_password(self) -> str | None:
        return os.getenv("TRIP_PASSWORD", "Hjj07270318")

    def _load_trip_module(self):
        if self._trip_module:
            return self._trip_module
        trip_dir = Path(BASE_DIR).parent / "kinit-trip"
        file_path = trip_dir / "xxx.py"
        trip_dir_text = str(trip_dir)
        if trip_dir_text not in sys.path:
            sys.path.insert(0, trip_dir_text)
        spec = importlib.util.spec_from_file_location("kinit_trip_xxx", file_path)
        module = importlib.util.module_from_spec(spec)
        assert spec and spec.loader
        spec.loader.exec_module(module)
        self._trip_module = module
        return module

    def build_query_payload(self, item: dict, travel_date: datetime) -> dict:
        return {
            "dept": item["departure_city"].upper(),
            "arr": item["arrival_city"].upper(),
            "fromdate": travel_date.strftime("%Y-%m-%d"),
            "currency": "CNY",
            "triptype": 1,
            "platformType": "B2B",
            "adtnum": 1,
            "chdnum": 0,
            "infnum": 0,
            "iata": "int",
        }

    async def query_flights(
            self,
            payload: dict,
            account: str | None,
            password: str | None,
            http_proxy: str | None = None,
            https_proxy: str | None = None
    ) -> tuple[bool, str, list]:
        module = self._load_trip_module()
        last_message = "采集失败"
        for attempt in range(1, REQUEST_MAX_RETRIES + 1):
            try:
                crawler = module.CrawlerTrip(
                    account=account,
                    password=password,
                    http_proxy=http_proxy,
                    https_proxy=https_proxy
                )
                query_result = await asyncio.to_thread(crawler.queryFlight, payload)
                if not isinstance(query_result, dict):
                    last_message = f"返回结果格式异常，第{attempt}次"
                elif query_result.get("code") != 200:
                    last_message = query_result.get("msg") or query_result.get("message") or "采集失败"
                else:
                    flight_result = await asyncio.to_thread(crawler.parseFlight, query_result.get("data"))
                    if isinstance(flight_result, list) and len(flight_result) > 0:
                        return True, f"success(retry={attempt})", flight_result
                    last_message = "采集成功但无有效航班数据"
            except Exception as e:
                last_message = f"采集异常：{str(e)}"
            if attempt < REQUEST_MAX_RETRIES:
                await asyncio.sleep(RETRY_SLEEP_SECONDS)
        return False, f"{last_message}（已重试{REQUEST_MAX_RETRIES}次）", []
