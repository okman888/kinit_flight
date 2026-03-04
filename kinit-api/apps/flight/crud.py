#!/usr/bin/python
# -*- coding: utf-8 -*-

from sqlalchemy.ext.asyncio import AsyncSession
from core.crud import DalBase
from . import models, schemas


class FlightTaskDal(DalBase):
    def __init__(self, db: AsyncSession):
        super(FlightTaskDal, self).__init__()
        self.db = db
        self.model = models.FlightTask
        self.schema = schemas.FlightTaskSimpleOut


class FlightItineraryDal(DalBase):
    def __init__(self, db: AsyncSession):
        super(FlightItineraryDal, self).__init__()
        self.db = db
        self.model = models.FlightItinerary
        self.schema = schemas.FlightItinerarySimpleOut


class FlightTaskLogDal(DalBase):
    def __init__(self, db: AsyncSession):
        super(FlightTaskLogDal, self).__init__()
        self.db = db
        self.model = models.FlightTaskLog
        self.schema = schemas.FlightTaskLogSimpleOut
