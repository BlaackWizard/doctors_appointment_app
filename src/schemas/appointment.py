import datetime
from datetime import time
from typing import Literal, Optional

from pydantic import BaseModel, Field, model_validator


class SScheduleCreate(BaseModel):
    day_of_week: Literal[
        "Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье",
    ] = Field(alias="День недели")
    start_time: time = Field(alias="Время начала визита")
    end_time: time = Field(alias="Время конца визита")

    @model_validator(mode="before")
    def check_schedule(cls, values):
        start_time = values.get("start_time")
        end_time = values.get("end_time")

        # Access alias-corrected field names
        if start_time and end_time and end_time <= start_time:
            raise ValueError(
                "Время завершения не может быть раньше или равно времени начала",
            )
        return values


class SAppointmentCreate(BaseModel):
    doctor_id: int = Field(alias="ID врача")
    schedule_id: int = Field(alias="ID слота")
    date_appointment: datetime.datetime = Field(alias="Время визита")


class SAppointmentResponse(BaseModel):
    doctor_id: int = Field(alias="ID врача")
    doctor_fullname: str = Field(alias="ФИО врача")
    schedule_id: int = Field(alias="ID слота")
    patient_id: int = Field(alias="ID пациента")
    patient_fullname: str = Field(alias="ФИО пациента")
    created_at: datetime.datetime = Field(alias="Дата создания (необязательно)")

    class Config:
        orm_mode = True


class SAllSchedule(BaseModel):
    doctor_id: int
    day_of_week: Literal["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]
    start_time: Optional[time] = None
    end_time: Optional[time] = None
