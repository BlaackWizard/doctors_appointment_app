from src.repos.appointment import AppointmentRepo
from src.repos.medical_card import DiagnosisRepo
from src.repos.payment import PaymentRepo
from src.repos.services import ServiceRepo
from src.repos.user import UserRepo
from src.services.report_services import ReportServices


def report_services():
    return ReportServices(
        appointment_repo=AppointmentRepo,
        payment_repo=PaymentRepo,
        user_repo=UserRepo,
        services_repo=ServiceRepo,
        diagnoses_repo=DiagnosisRepo,
    )
