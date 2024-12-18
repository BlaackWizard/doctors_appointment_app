from typing import Annotated

from fastapi import APIRouter, Depends

from src.services.create_appointment_service import AppointmentService

from ...schemas.appointment import SScheduleCreate
from .dependencies import appointment_service

router = APIRouter(prefix='/doctors', tags=['Врачи'])


@router.post('/create-schedule')
async def create_schedule_endpoint(
    doctor_data: SScheduleCreate,
    appointment_service: Annotated[AppointmentService, Depends(appointment_service)],
):
    appointment = await appointment_service.create_schedule(doctor_data)
    return appointment
