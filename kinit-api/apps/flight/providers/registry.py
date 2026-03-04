#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import annotations

from .base import FlightProvider


class FlightProviderRegistry:
    def __init__(self):
        self._providers: dict[str, FlightProvider] = {}

    def register(self, provider: FlightProvider) -> None:
        self._providers[provider.channel] = provider

    def get(self, channel: str) -> FlightProvider:
        provider = self._providers.get(channel)
        if not provider:
            supported = ", ".join(sorted(self._providers.keys()))
            raise ValueError(f"未注册的采集渠道: {channel}，已支持: {supported or '无'}")
        return provider

    def all_channels(self) -> list[str]:
        return sorted(self._providers.keys())


flight_provider_registry = FlightProviderRegistry()
