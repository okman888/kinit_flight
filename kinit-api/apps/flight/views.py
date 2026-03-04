#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import uuid
from fastapi import APIRouter, Depends, Body
from sqlalchemy.orm import joinedload

from core.exception import CustomException
from utils.response import SuccessResponse
from utils import status
from apps.vadmin.auth.utils.current import AllUserAuth
from apps.vadmin.auth.utils.validation.auth import Auth
from . import schemas, params, crud, models, service
from .providers import flight_provider_registry

app = APIRouter()


@app.get("/tasks", summary="获取航班采集任务列表")
async def get_flight_tasks(p: params.FlightTaskParams = Depends(), auth: Auth = Depends(AllUserAuth())):
    model = models.FlightTask
    options = [joinedload(model.create_user)]
    datas, count = await crud.FlightTaskDal(auth.db).get_datas(
        **p.dict(),
        v_options=options,
        v_schema=schemas.FlightTaskListOut,
        v_return_count=True
    )
    return SuccessResponse(datas, count=count)


@app.get("/tasks/{task_id}", summary="获取航班采集任务详情")
async def get_flight_task(task_id: str, auth: Auth = Depends(AllUserAuth())):
    model = models.FlightTask
    options = [joinedload(model.create_user)]
    data = await crud.FlightTaskDal(auth.db).get_data(
        task_id=task_id,
        v_options=options,
        v_schema=schemas.FlightTaskDetailOut
    )
    return SuccessResponse(data)


@app.post("/tasks", summary="创建并执行航班采集任务")
async def create_flight_task(
        data: schemas.FlightTaskCreateIn,
        auth: Auth = Depends(AllUserAuth())
):
    if data.channel not in flight_provider_registry.all_channels():
        raise CustomException(
            msg=f"不支持的采集渠道: {data.channel}，可选渠道: {', '.join(flight_provider_registry.all_channels())}",
            code=status.HTTP_ERROR
        )
    task_id = str(uuid.uuid4().hex)[:20]
    task_name = data.task_name or f"航班采集任务-{task_id}"
    task_payload = {
        "channel": data.channel,
        "items": [item.model_dump() for item in data.items]
    }
    task_obj = await crud.FlightTaskDal(auth.db).create_data(
        data={
            "task_id": task_id,
            "task_name": task_name,
            "channel": data.channel,
            "status": "collecting",
            "message": "任务采集中",
            "task_payload": json.dumps(task_payload, ensure_ascii=False),
            "created_by_id": auth.user.id
        },
        v_return_obj=True
    )
    service.submit_flight_task(
        task_id=task_id,
        account=data.channel_account,
        password=data.channel_password,
        http_proxy=data.http_proxy,
        https_proxy=data.https_proxy
    )
    return SuccessResponse(schemas.FlightTaskSimpleOut.model_validate(task_obj).model_dump())


@app.post("/tasks/{task_id}/run", summary="重新执行航班采集任务")
async def run_flight_task(task_id: str, failed_only: bool = True, auth: Auth = Depends(AllUserAuth())):
    task = await crud.FlightTaskDal(auth.db).get_data(task_id=task_id)
    if task.status == "collecting":
        raise CustomException(msg="任务正在采集中，请勿重复提交", code=status.HTTP_ERROR)
    if failed_only and task.failed_requests <= 0 and task.status != "failed":
        raise CustomException(msg="当前任务无失败请求，无需重试", code=status.HTTP_ERROR)
    task.status = "collecting"
    task.message = "任务采集中（失败请求重试）" if failed_only else "任务采集中（全量重跑）"
    await auth.db.commit()
    service.submit_flight_task(task_id, retry_failed_only=failed_only)
    return SuccessResponse("任务已重新提交")


@app.get("/tasks/{task_id}/logs", summary="获取任务采集日志")
async def get_flight_task_logs(task_id: str, auth: Auth = Depends(AllUserAuth())):
    await crud.FlightTaskDal(auth.db).get_data(task_id=task_id)
    try:
        datas = await crud.FlightTaskLogDal(auth.db).get_datas(
            limit=0,
            task_id=task_id,
            v_order="desc",
            v_order_field="create_datetime",
            v_schema=schemas.FlightTaskLogSimpleOut
        )
    except Exception:
        datas = []
    return SuccessResponse(datas)


@app.delete("/tasks", summary="批量删除航班采集任务")
async def delete_flight_tasks(ids: list[int] = Body(..., embed=True), auth: Auth = Depends(AllUserAuth())):
    await crud.FlightTaskDal(auth.db).delete_datas(ids, v_soft=False)
    return SuccessResponse("删除成功")


@app.get("/tasks/{task_id}/export", summary="导出指定任务结果Excel")
async def export_flight_task(task_id: str, auth: Auth = Depends(AllUserAuth())):
    await crud.FlightTaskDal(auth.db).get_data(task_id=task_id)
    result = await service.export_task_to_excel(task_id)
    return SuccessResponse(result)


@app.get("/results", summary="获取航班采集结果列表")
async def get_flight_results(p: params.FlightItineraryParams = Depends(), auth: Auth = Depends(AllUserAuth())):
    datas, count = await crud.FlightItineraryDal(auth.db).get_datas(
        **p.dict(),
        v_schema=schemas.FlightItineraryListOut,
        v_return_count=True
    )
    return SuccessResponse(datas, count=count)
