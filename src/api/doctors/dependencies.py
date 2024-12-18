from src.models.appointment import AppointmentModel
from src.repos.doctor_schedule import DoctorScheduleRepo
from src.repos.user import UserRepo
from src.services.create_appointment_service import AppointmentService


def appointment_service():
    return AppointmentService(
        appointment_repo=AppointmentModel,
        doctor_schedule_repo=DoctorScheduleRepo,
        user_repo=UserRepo,
    )
