#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime


class FlightProvider(ABC):
    """航班采集插件统一协议。"""

    @property
    @abstractmethod
    def channel(self) -> str:
        """插件渠道标识，例如 hk.trip.com。"""

    @property
    @abstractmethod
    def default_account(self) -> str | None:
        """渠道默认账号，可为 None。"""

    @property
    @abstractmethod
    def default_password(self) -> str | None:
        """渠道默认密码，可为 None。"""

    @abstractmethod
    def build_query_payload(self, item: dict, travel_date: datetime) -> dict:
        """构建渠道查询参数。"""

    @abstractmethod
    async def query_flights(
            self,
            payload: dict,
            account: str | None,
            password: str | None,
            http_proxy: str | None = None,
            https_proxy: str | None = None
    ) -> tuple[bool, str, list]:
        """执行查询并返回统一结构 (成功标识, 描述, 航班列表)。"""
