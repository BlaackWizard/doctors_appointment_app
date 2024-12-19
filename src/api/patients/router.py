from datetime import time
from typing import Annotated, Literal, Optional

from fastapi import APIRouter, Depends, Response

from src.api.doctors.dependencies import (appointment_service,
                                          medical_card_services)
from src.schemas.auth import SUserLogin, SUserRegister
from src.services.auth_service import UserAuth, get_current_user

from ...schemas.appointment import SAppointmentCreate
from ...services.create_appointment_service import AppointmentService
from ...services.medical_card_service import MedicalCardService
from .dependencies import user_services

router = APIRouter(prefix='/patient', tags=['Пациенты'])


@router.post('/register')
async def register_user_endpoint(
    user_data: SUserRegister,
    user_services: Annotated[UserAuth, Depends(user_services)],
):
    await user_services.register_user(
        user_data=user_data,
    )
    return Response("Пользователь успешно создан")


@router.post("/login")
async def login_user_endpoint(
    response: Response,
    user_data: SUserLogin,
    user_services: Annotated[UserAuth, Depends(user_services)],
):
    access_token = await user_services.login_user(user_data)
    response.set_cookie("user_access_token", access_token, httponly=True)

    return {"access_token": access_token}


@router.get("/show-all-slots/{doctor_id}/{date}")
async def show_all_available_slots(
    appointment_services: Annotated[AppointmentService, Depends(appointment_service)],
    doctor_id: int,
    day_of_week: Literal["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"],
    start_time: Optional[time] = None,
    end_time: Optional[time] = None,
):
    return await appointment_services.show_all_schedules_doctors(
        doctor_id=doctor_id,
        day_of_week=day_of_week,
        start_time=start_time,
        end_time=end_time,
    )


@router.post("/appointment-with-the-doctor/")
async def appointment_with_the_doctor_endpoint(
    appointment_services: Annotated[AppointmentService, Depends(appointment_service)],
    doctor_data: SAppointmentCreate,
    user: str = Depends(get_current_user),

):

    await appointment_services.create_appointment(doctor_data, user)
    return 'Создана новая запись'


@router.post("/history-appointments")
async def history_appointments_endpoint(
    appointment_services: Annotated[AppointmentService, Depends(appointment_service)],
    user: str = Depends(get_current_user),
):
    return await appointment_services.show_all_appointments(user.id)


@router.post("/create-medical-card")
async def create_medical_card_endpoint(
    med_services: Annotated[MedicalCardService, Depends(medical_card_services)],
    doctor_id: int,
    user: str = Depends(get_current_user),
):

    return await med_services.create_medical_card(patient_id=user.id, doctor_id=doctor_id)


@router.get('/my-medical-card')
async def get_my_medical_card_endpoint(
    med_services: Annotated[MedicalCardService, Depends(medical_card_services)],
    user: str = Depends(get_current_user),
):
    return await med_services.get_medical_card(user_id=user.id)
