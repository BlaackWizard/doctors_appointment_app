from src.repos.appointment import AppointmentRepo
from src.repos.doctor_schedule import DoctorScheduleRepo
from src.repos.user import UserRepo
from src.services.auth_service import UserAuth


def user_services():
    return UserAuth(repo=UserRepo, appointment_repo=AppointmentRepo, doctor_schedule_repo=DoctorScheduleRepo)
