from typing import Annotated

from fastapi import APIRouter, Depends

from src.services.create_appointment_service import AppointmentService

from ...models.user import UserModel
from ...schemas.appointment import SScheduleCreate
from ...schemas.medical_card import SDiagnosis, SVisits
from ...services.auth_service import get_current_doctor
from ...services.medical_card_service import DiagnoseService, VisitService
from .dependencies import appointment_service, diagnose_service, visit_service

router = APIRouter(prefix='/doctors', tags=['Врачи'])


@router.post('/create-schedule')
async def create_schedule_endpoint(
    doctor_data: SScheduleCreate,
    appointment_service: Annotated[AppointmentService, Depends(appointment_service)],
    user: UserModel = Depends(get_current_doctor),
):

    appointment = await appointment_service.create_schedule(doctor=user, doctor_data=doctor_data)
    return appointment


@router.post('/change-status-schedule')
async def change_status_schedule_endpoint(
    appointment_service: Annotated[AppointmentService, Depends(appointment_service)],
    schedule_id: int,
    user: UserModel = Depends(get_current_doctor),
):
    return await appointment_service.change_status_schedule(doctor=user, schedule_id=schedule_id)


@router.post('/create-diagnose')
async def create_diagnose_endpoint(
    diagnose_service: Annotated[DiagnoseService, Depends(diagnose_service)],
    diagnose_data: SDiagnosis,
    user: UserModel = Depends(get_current_doctor),
):
    return await diagnose_service.create_diagnose(doctor_id=user.id, diagnose_data=diagnose_data)


@router.post("/create-visit")
async def create_visit_endpoint(
    visit_service: Annotated[VisitService, Depends(visit_service)],
    visit_data: SVisits,
    user: UserModel = Depends(get_current_doctor),
):
    return await visit_service.create_visit(doctor_id=user.id, visit_data=visit_data)
