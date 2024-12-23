from typing import Annotated

from fastapi import APIRouter, Depends

from src.services.create_appointment_service import AppointmentService

from ...models.user import UserModel
from ...schemas.analyze import SAnalyzeRequest
from ...schemas.appointment import SScheduleCreate
from ...schemas.medical_card import SDiagnosis, SProcedure, SVisits
from ...services.analyze_service import AnalyzeService
from ...services.auth_service import get_current_doctor
from ...services.diagnose_service import DiagnoseService
from ...services.procedure_service import ProcedureService
from ...services.visit_service import VisitService
from .dependencies import (analyze_service, appointment_service,
                           diagnose_service, procedure_service, visit_service)

router = APIRouter(prefix='/doctors', tags=['Врачи'])


@router.post('/create-schedule')
async def create_schedule_endpoint(
    doctor_data: SScheduleCreate,
    appointment_service: Annotated[AppointmentService, Depends(appointment_service)],
    user: UserModel = Depends(get_current_doctor),
):

    appointment = await appointment_service.create_schedule(doctor=user, doctor_data=doctor_data)
    return appointment


@router.post('/update-schedule')
async def update_schedule_endpoint(
    doctor_data: SScheduleCreate,
    schedule_id: int,
    appointment_service: Annotated[AppointmentService, Depends(appointment_service)],
    user: UserModel = Depends(get_current_doctor),
):
    return await appointment_service.update_schedule(doctor=user, doctor_data=doctor_data, schedule_id=schedule_id)


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


@router.post('/update-diagnose')
async def update_diagnose_endpoint(
    diagnose_service: Annotated[DiagnoseService, Depends(diagnose_service)],
    diagnose_data: SDiagnosis,
    diagnose_id: int,
    user: UserModel = Depends(get_current_doctor),
):
    return await diagnose_service.update_diagnose(
        doctor_id=user.id,
        diagnose_data=diagnose_data,
        diagnose_id=diagnose_id,
    )


@router.post("/create-visit")
async def create_visit_endpoint(
    visit_service: Annotated[VisitService, Depends(visit_service)],
    visit_data: SVisits,
    user: UserModel = Depends(get_current_doctor),
):
    return await visit_service.create_visit(doctor_id=user.id, visit_data=visit_data)


@router.post("/create-procedure")
async def create_procedure_endpoint(
    procedure_data: SProcedure,
    user_id: int,
    procedure_service: Annotated[ProcedureService, Depends(procedure_service)],
    doctor: UserModel = Depends(get_current_doctor),

):

    return await procedure_service.create_procedure(
        user_id=user_id,
        doctor=doctor,
        procedure_data=procedure_data,
    )


@router.post("/update-procedure")
async def update_procedure_endpoint(
    procedure_data: SProcedure,
    procedure_id: int,
    user_id: int,
    procedure_service: Annotated[ProcedureService, Depends(procedure_service)],
    doctor: UserModel = Depends(get_current_doctor),
):
    await procedure_service.update_procedure(
        user_id=user_id,
        doctor=doctor,
        procedure_data=procedure_data,
        procedure_id=procedure_id,
    )


@router.post('/create-analyze')
async def create_analyze(
    analyze_services: Annotated[AnalyzeService, Depends(analyze_service)],
    analyze_data: SAnalyzeRequest = Depends(),
    doctor: UserModel = Depends(get_current_doctor),
):
    return await analyze_services.add_analyze(doctor_id=doctor.id, analyze_data=analyze_data)


@router.get("/my-appointments")
async def get_doctors_appointments(
    appointment_service: Annotated[AppointmentService, Depends(appointment_service)],
    doctor: UserModel = Depends(get_current_doctor),
):
    return await appointment_service.my_appointments(doctor_id=doctor.id)
