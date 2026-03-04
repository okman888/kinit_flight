#!/usr/bin/python
# -*- coding: utf-8 -*-

from pydantic import BaseModel, ConfigDict, Field
from core.data_types import DatetimeStr, DateStr
from apps.vadmin.auth.schemas import UserSimpleOut


class FlightTaskItemIn(BaseModel):
    departure_city: str = Field(..., title="出发城市代码")
    departure_city_name: str | None = Field(default=None, title="出发城市名称")
    arrival_city: str = Field(..., title="到达城市代码")
    arrival_city_name: str | None = Field(default=None, title="到达城市名称")
    start_date: DateStr = Field(..., title="开始日期")
    end_date: DateStr = Field(..., title="结束日期")


class FlightTaskCreateIn(BaseModel):
    task_name: str | None = Field(default=None, title="任务名称")
    channel: str = Field(default="hk.trip.com", title="采集渠道")
    channel_account: str | None = Field(default=None, title="渠道账号")
    channel_password: str | None = Field(default=None, title="渠道密码")
    http_proxy: str | None = Field(default=None, title="HTTP代理")
    https_proxy: str | None = Field(default=None, title="HTTPS代理")
    items: list[FlightTaskItemIn] = Field(default_factory=list, min_length=1, title="采集项")


class FlightTaskSimpleOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    task_id: str
    task_name: str | None
    channel: str
    status: str
    message: str | None
    total_routes: int
    total_days: int
    total_requests: int
    success_requests: int
    failed_requests: int
    result_count: int
    started_at: DatetimeStr | None = None
    finished_at: DatetimeStr | None = None
    result_file_url: str | None = None
    create_datetime: DatetimeStr
    update_datetime: DatetimeStr


class FlightTaskListOut(FlightTaskSimpleOut):
    model_config = ConfigDict(from_attributes=True)

    create_user: UserSimpleOut | None = None


class FlightTaskDetailOut(FlightTaskListOut):
    model_config = ConfigDict(from_attributes=True)

    task_payload: str


class FlightItinerarySimpleOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    task_id: str
    create_time: str
    row_id: str
    travel_date: DatetimeStr
    departure_city: str
    departure_city_name: str | None
    departure_time: str | None
    arrival_city: str
    arrival_city_name: str | None
    arrival_time: str | None
    duration: int | None
    stopover: str | None
    stopover_duration: str | None
    min_price: int | None
    min_price_tax: int | None
    min_price_discount: str | None
    min_business_price: int | None
    min_business_price_tax: int | None
    departure_airport: str | None
    departure_airport_name: str | None
    departure_terminal: str | None
    arrival_airport: str | None
    arrival_airport_name: str | None
    arrival_terminal: str | None
    seat_left: str | None
    default_cabin: str | None
    segment_list: str | None
    economy_policies: str | None
    business_policies: str | None
    flights_info: str | None
    data_source: str


class FlightItineraryListOut(FlightItinerarySimpleOut):
    model_config = ConfigDict(from_attributes=True)

    create_datetime: DatetimeStr


class FlightTaskLogSimpleOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    task_id: str
    departure_city: str
    arrival_city: str
    travel_date: DatetimeStr
    status: str
    execute_ms: int
    retry_count: int
    message: str | None
    create_datetime: DatetimeStr
