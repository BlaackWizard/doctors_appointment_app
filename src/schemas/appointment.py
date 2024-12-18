from datetime import datetime, time
from typing import Literal

from pydantic import BaseModel, Field


class SScheduleCreate(BaseModel):
    day_of_week: Literal["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]
    start_time: time
    end_time: time


class SAppointmentCreate(BaseModel):
    doctor_id: int
    schedule_id: int
    patient_id: int
    date: datetime = Field(default=datetime.now())


class SAppointmentResponse(BaseModel):
    doctor_id: int
    doctor_fullname: str
    schedule_id: int
    patient_id: int
    patient_fullname: str
    created_at: datetime

    class Config:
        orm_mode = True
