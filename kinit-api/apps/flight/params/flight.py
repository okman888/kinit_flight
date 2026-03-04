#!/usr/bin/python
# -*- coding: utf-8 -*-

from fastapi import Depends
from core.dependencies import Paging, QueryParams


class FlightTaskParams(QueryParams):
    def __init__(
            self,
            params: Paging = Depends(),
            task_id: str = None,
            task_name: str = None,
            channel: str = None,
            status: str = None
    ):
        super().__init__(params)
        self.v_order = "desc"
        self.v_order_field = "create_datetime"
        self.task_id = ("like", task_id)
        self.task_name = ("like", task_name)
        self.channel = channel
        self.status = status


class FlightItineraryParams(QueryParams):
    def __init__(
            self,
            params: Paging = Depends(),
            task_id: str = None,
            departure_city: str = None,
            arrival_city: str = None,
            travel_date: str = None,
            data_source: str = None
    ):
        super().__init__(params)
        self.v_order = "desc"
        self.v_order_field = "create_datetime"
        self.task_id = task_id
        self.departure_city = departure_city
        self.arrival_city = arrival_city
        self.travel_date = ("date", travel_date) if travel_date else None
        self.data_source = data_source
