import datetime
from datetime import date, time
from typing import Literal

from pydantic import BaseModel, model_validator


class SScheduleCreate(BaseModel):
    date: date
    day_of_week: Literal["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]
    start_time: time
    end_time: time

    @model_validator(mode='before')
    def check_schedule(cls, values):
        schedule_date = values.get('date')

        if isinstance(schedule_date, str):
            schedule_date = date.fromisoformat(schedule_date)

        today = datetime.date.today()
        if schedule_date < today:
            raise ValueError("Дата не должна быть меньше чем сегодняшняя дата")

        start_time = values.get('start_time')
        end_time = values.get('end_time')
        if start_time and end_time and end_time <= start_time:
            raise ValueError("Время завершения не может быть раньше или равно времени начала")

        day_of_week = values.get('day_of_week')
        if schedule_date and day_of_week:
            date_week = schedule_date.strftime("%A")

            day_mapping = {
                'Monday': 'Понедельник',
                'Tuesday': 'Вторник',
                'Wednesday': 'Среда',
                'Thursday': 'Четверг',
                'Friday': 'Пятница',
                'Saturday': 'Суббота',
                'Sunday': 'Воскресенье',
            }

            if day_mapping.get(date_week) != day_of_week:
                raise ValueError("День недели не совпадает с датой")

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
