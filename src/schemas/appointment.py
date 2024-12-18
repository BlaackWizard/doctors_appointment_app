from datetime import datetime
from pydantic import BaseModel


class SScheduleCreate(BaseModel):
    doctor_id: int
    date: datetime


class SAppointmentCreate(BaseModel):
    doctor_id: int
    schedule_id: int
    patient_id: int


class SAppointmentResponse(BaseModel):
    doctor_id: int
    schedule_id: int
    patient_id: int
    created_at: datetime

    class Config:
        orm_mode = True
