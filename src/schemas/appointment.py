import datetime
from datetime import time
from typing import Literal

from pydantic import BaseModel, model_validator


class SScheduleCreate(BaseModel):
    day_of_week: Literal["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]
    start_time: time
    end_time: time

    @model_validator(mode='before')
    def check_schedule(cls, values):

        start_time = values.get('start_time')
        end_time = values.get('end_time')
        if start_time and end_time and end_time <= start_time:
            raise ValueError("Время завершения не может быть раньше или равно времени начала")

        return values


class SAppointmentCreate(BaseModel):
    doctor_id: int
    schedule_id: int
    date: datetime.datetime


class SAppointmentResponse(BaseModel):
    doctor_id: int
    doctor_fullname: str
    schedule_id: int
    patient_id: int
    patient_fullname: str
    created_at: datetime.datetime

    class Config:
        orm_mode = True
