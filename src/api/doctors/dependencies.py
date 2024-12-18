from src.repos.appointment import AppointmentRepo
from src.repos.doctor_schedule import DoctorScheduleRepo
from src.repos.medical_card import DiagnosisRepo, MedicalCardRepo, VisitsRepo
from src.repos.user import UserRepo
from src.services.create_appointment_service import AppointmentService
from src.services.medical_card_service import (DiagnoseService,
                                               MedicalCardService,
                                               VisitService)


def appointment_service():
    return AppointmentService(
        appointment_repo=AppointmentRepo,
        doctor_schedule_repo=DoctorScheduleRepo,
        user_repo=UserRepo,
    )


def medical_card_services():
    return MedicalCardService(
        medical_card_repo=MedicalCardRepo,
        diagnosis_repo=DiagnosisRepo,
        visits_repo=VisitsRepo,
        user_repo=UserRepo,
    )


def diagnose_service():
    return DiagnoseService(
        diagnosis_repo=DiagnosisRepo,
        medical_card_repo=MedicalCardRepo,
    )


def visit_service():
    return VisitService(
        visits_repo=VisitsRepo,
        medical_repo=MedicalCardRepo,
    )
