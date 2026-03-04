#!/usr/bin/python
# -*- coding: utf-8 -*-

from .registry import flight_provider_registry
from .trip_provider import TripProvider


flight_provider_registry.register(TripProvider())

__all__ = ["flight_provider_registry"]
