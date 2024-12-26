from src.repos.appointment import AppointmentRepo
from src.repos.doctor_schedule import DoctorScheduleRepo
from src.repos.medical_card import (AnalyzeRepo, DiagnosisRepo,
                                    MedicalCardRepo, ProcedureRepo, VisitsRepo)
from src.repos.user import UserRepo
from src.services.analyze_service import AnalyzeService
from src.services.create_appointment_service import AppointmentService
from src.services.diagnose_service import DiagnoseService
from src.services.medical_card_service import MedicalCardService
from src.services.procedure_service import ProcedureService
from src.services.visit_service import VisitService


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
        procedure_repo=ProcedureRepo,
        appointment_repo=AppointmentRepo,
        analyze_repo=AnalyzeRepo,
    )


def diagnose_service():
    return DiagnoseService(
        diagnosis_repo=DiagnosisRepo,
        medical_card_repo=MedicalCardRepo,
    )


def visit_service():
    return VisitService(
        visits_repo=VisitsRepo,
        user_repo=UserRepo,
        appointment_repo=AppointmentRepo,
        medical_card_repo=MedicalCardRepo,
    )


def procedure_service():
    return ProcedureService(
        medical_card_repo=MedicalCardRepo,
        test_repo=AnalyzeRepo,
        procedure_repo=ProcedureRepo,
        user_repo=UserRepo,
    )


def analyze_service():
    return AnalyzeService(
        user_repo=UserRepo,
        medical_card_repo=MedicalCardRepo,
        analyze_repo=AnalyzeRepo,
    )
