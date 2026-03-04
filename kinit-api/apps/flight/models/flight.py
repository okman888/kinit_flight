#!/usr/bin/python
# -*- coding: utf-8 -*-

from datetime import datetime
from sqlalchemy import String, Integer, DateTime, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from db.db_base import BaseModel
from apps.vadmin.auth.models import VadminUser


class FlightTask(BaseModel):
    __tablename__ = "flight_task"
    __table_args__ = ({'comment': '航班采集任务表'})

    task_id: Mapped[str] = mapped_column(String(32), unique=True, index=True, comment="任务ID")
    task_name: Mapped[str | None] = mapped_column(String(100), nullable=True, comment="任务名称")
    channel: Mapped[str] = mapped_column(String(50), default="hk.trip.com", comment="采集渠道")
    status: Mapped[str] = mapped_column(String(20), default="pending", index=True, comment="任务状态")
    message: Mapped[str | None] = mapped_column(Text, nullable=True, comment="任务执行说明")
    task_payload: Mapped[str] = mapped_column(Text, comment="任务参数JSON")

    total_routes: Mapped[int] = mapped_column(Integer, default=0, comment="航线总数")
    total_days: Mapped[int] = mapped_column(Integer, default=0, comment="采集天数")
    total_requests: Mapped[int] = mapped_column(Integer, default=0, comment="请求总数")
    success_requests: Mapped[int] = mapped_column(Integer, default=0, comment="成功请求数")
    failed_requests: Mapped[int] = mapped_column(Integer, default=0, comment="失败请求数")
    result_count: Mapped[int] = mapped_column(Integer, default=0, comment="结果总条数")

    started_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True, comment="开始执行时间")
    finished_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True, comment="结束执行时间")
    result_file_url: Mapped[str | None] = mapped_column(String(255), nullable=True, comment="结果文件地址")

    created_by_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey("vadmin_auth_user.id", ondelete='SET NULL'),
        nullable=True,
        comment="创建人"
    )
    create_user: Mapped[VadminUser | None] = relationship(foreign_keys=created_by_id)

    itineraries: Mapped[list["FlightItinerary"]] = relationship(back_populates="task")
    logs: Mapped[list["FlightTaskLog"]] = relationship(back_populates="task")


class FlightItinerary(BaseModel):
    __tablename__ = "flight_itinerary"
    __table_args__ = ({'comment': '航班采集结果表'})

    task_db_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("flight_task.id", ondelete='CASCADE'),
        index=True,
        comment="任务主键ID"
    )
    task_id: Mapped[str] = mapped_column(String(32), index=True, comment="任务ID")

    create_time: Mapped[str] = mapped_column(String(32), comment="采集时间(ods格式)")
    row_id: Mapped[str] = mapped_column(String(32), unique=True, index=True, comment="数据ID(ods字段id)")
    travel_date: Mapped[DateTime] = mapped_column(DateTime, index=True, comment="出发日期")
    departure_city: Mapped[str] = mapped_column(String(10), index=True, comment="出发城市代码")
    departure_city_name: Mapped[str | None] = mapped_column(String(50), nullable=True, comment="出发城市名称")
    departure_time: Mapped[str | None] = mapped_column(String(25), nullable=True, comment="出发时间")
    arrival_city: Mapped[str] = mapped_column(String(10), index=True, comment="到达城市代码")
    arrival_city_name: Mapped[str | None] = mapped_column(String(50), nullable=True, comment="到达城市名称")
    arrival_time: Mapped[str | None] = mapped_column(String(25), nullable=True, comment="到达时间")
    duration: Mapped[int | None] = mapped_column(Integer, nullable=True, comment="总时长(分钟)")
    stopover: Mapped[str | None] = mapped_column(String(255), nullable=True, comment="经停信息")
    stopover_duration: Mapped[str | None] = mapped_column(String(255), nullable=True, comment="经停时长")
    min_price: Mapped[int | None] = mapped_column(Integer, nullable=True, comment="最低经济舱价格")
    min_price_tax: Mapped[int | None] = mapped_column(Integer, nullable=True, comment="最低经济舱税费")
    min_price_discount: Mapped[str | None] = mapped_column(String(32), nullable=True, comment="最低经济舱折扣")
    min_business_price: Mapped[int | None] = mapped_column(Integer, nullable=True, comment="最低商务舱价格")
    min_business_price_tax: Mapped[int | None] = mapped_column(Integer, nullable=True, comment="最低商务舱税费")
    departure_airport: Mapped[str | None] = mapped_column(String(12), nullable=True, comment="出发机场代码")
    departure_airport_name: Mapped[str | None] = mapped_column(String(64), nullable=True, comment="出发机场名称")
    departure_terminal: Mapped[str | None] = mapped_column(String(32), nullable=True, comment="出发航站楼")
    arrival_airport: Mapped[str | None] = mapped_column(String(12), nullable=True, comment="到达机场代码")
    arrival_airport_name: Mapped[str | None] = mapped_column(String(64), nullable=True, comment="到达机场名称")
    arrival_terminal: Mapped[str | None] = mapped_column(String(32), nullable=True, comment="到达航站楼")
    seat_left: Mapped[str | None] = mapped_column(String(32), nullable=True, comment="剩余座位")
    default_cabin: Mapped[str | None] = mapped_column(String(64), nullable=True, comment="默认舱位")
    segment_list: Mapped[str | None] = mapped_column(Text, nullable=True, comment="航段结构JSON")
    economy_policies: Mapped[str | None] = mapped_column(Text, nullable=True, comment="经济舱政策")
    business_policies: Mapped[str | None] = mapped_column(Text, nullable=True, comment="商务舱政策")
    flights_info: Mapped[str | None] = mapped_column(Text, nullable=True, comment="航班摘要")
    data_source: Mapped[str] = mapped_column(String(50), default="hk.trip.com", comment="数据来源")
    raw_payload: Mapped[str | None] = mapped_column(Text, nullable=True, comment="原始数据JSON")

    task: Mapped[FlightTask] = relationship(back_populates="itineraries")


class FlightTaskLog(BaseModel):
    __tablename__ = "flight_task_log"
    __table_args__ = ({'comment': '航班采集任务执行日志表'})

    task_db_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("flight_task.id", ondelete='CASCADE'),
        index=True,
        comment="任务主键ID"
    )
    task_id: Mapped[str] = mapped_column(String(32), index=True, comment="任务ID")
    departure_city: Mapped[str] = mapped_column(String(10), index=True, comment="出发城市代码")
    arrival_city: Mapped[str] = mapped_column(String(10), index=True, comment="到达城市代码")
    travel_date: Mapped[DateTime] = mapped_column(DateTime, index=True, comment="出发日期")
    status: Mapped[str] = mapped_column(String(20), index=True, comment="执行状态")
    execute_ms: Mapped[int] = mapped_column(Integer, default=0, comment="执行耗时(ms)")
    retry_count: Mapped[int] = mapped_column(Integer, default=0, comment="自动重试次数")
    message: Mapped[str | None] = mapped_column(Text, nullable=True, comment="执行结果信息")

    task: Mapped[FlightTask] = relationship(back_populates="logs")
