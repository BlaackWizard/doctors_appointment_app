import datetime
from collections import defaultdict
from dataclasses import dataclass
from datetime import time

from src.config import settings
from src.exceptions.appointment.appointment import (
    AppointmentAlreadyExistsException, NotFoundAppointmentException)
from src.exceptions.appointment.doctor import (
    NotFoundDoctorOrUserIsNotDoctorException, ThisIsAnotherDoctorException,
    ThisIsNotYoursScheduleException)
from src.exceptions.appointment.schedule import (
    DoctorCanNotChangeHisSlotWhilePatientsNotDoneTheirAppointmentException,
    NotFoundScheduleException, SlotIsOccupiedException,
    ThisScheduleAlreadyExistsException)
from src.exceptions.auth.user import NotFoundUserByIDException
from src.exceptions.user.roles import YouAreNotDoctorException
from src.repos.base import BaseRepo
from src.tasks.send_email import send_confirmation_email
from src.tasks.tasks_token import create_url_safe_token


def format_schedule(slots):
    schedule = defaultdict(list)
    for slot in slots:
        day = slot.day_of_week
        start_time = slot.start_time.strftime("%H:%M")
        end_time = slot.end_time.strftime("%H:%M")
        is_available = "Доступен" if slot.is_available else "Занят"

        schedule[day].append({
            "id": slot.id,
            "start_time": start_time,
            "end_time": end_time,
            "status": is_available,
        })

    return dict(schedule)


@dataclass
class AppointmentService:
    doctor_schedule_repo: BaseRepo
    appointment_repo: BaseRepo
    user_repo: BaseRepo

    async def _check_and_create_schedule(self, user, doctor_id, doctor_data):
        doctor = await self.user_repo.find_one(id=doctor_id)
        if not doctor:
            raise NotFoundUserByIDException().message

        schedule = await self.doctor_schedule_repo.find_one(
            doctor_id=doctor_id,
            day_of_week=doctor_data.day_of_week,
            start_time=doctor_data.start_time,
            end_time=doctor_data.end_time,
        )
        if schedule:
            raise ThisScheduleAlreadyExistsException().message

        schedule = await self.doctor_schedule_repo.add(
            doctor_id=doctor_id,
            day_of_week=doctor_data.day_of_week,
            start_time=doctor_data.start_time,
            end_time=doctor_data.end_time,
        )
        return schedule

    async def create_schedule(self, user, doctor_id, doctor_data):
        if user.role == 'admin':
            return await self._check_and_create_schedule(user, doctor_id, doctor_data)

        if user.role == 'doctor' and user.id == doctor_id:
            return await self._check_and_create_schedule(user, user.id, doctor_data)

        raise YouAreNotDoctorException().message

    async def check_schedule(self, doctor_id, schedule_id):
        doctor = await self.user_repo.find_one(id=doctor_id, role='doctor')
        if not doctor:
            raise NotFoundDoctorOrUserIsNotDoctorException().message

        schedule = await self.doctor_schedule_repo.find_one(id=schedule_id)
        if not schedule:
            raise NotFoundScheduleException().message

        if schedule.doctor_id != doctor.id:
            raise ThisIsNotYoursScheduleException().message

        appointments = await self.appointment_repo.find_all_by_filters(
            schedule_id=schedule_id,
            is_verified=True,
            status='ожидание',
        )

        if appointments:
            raise DoctorCanNotChangeHisSlotWhilePatientsNotDoneTheirAppointmentException().message
        return True

    async def update_schedule(self, doctor_id, user, doctor_data, schedule_id):
        check = await self.check_schedule(doctor_id, schedule_id)
        if not check:
            return

        await self.doctor_schedule_repo.update(
            model_id=schedule_id,
            day_of_week=doctor_data.day_of_week,
            start_time=doctor_data.start_time,
            end_time=doctor_data.end_time,
        )
        return 'Обновлены данные слота'

    async def delete_schedule(self, doctor_id, user, schedule_id):
        check = await self.check_schedule(doctor_id, schedule_id)
        if not check:
            return

        await self.doctor_schedule_repo.delete_one(model_id=schedule_id)
        return 'Удален слот'

    async def format_appointment(self, appointments):
        slots = defaultdict(list)

        for appointment in appointments:
            user = await self.user_repo.find_one(id=appointment.patient_id)
            doctor = await self.user_repo.find_one(id=appointment.doctor_id)

            slots[user.full_name].append({
                "id": appointment.id,
                "patient_id": appointment.patient_id,
                "doctor_id": appointment.doctor_id,
                "doctor_fullname": doctor.full_name,
                "status": appointment.status,
                "is_verified": appointment.is_verified,
            })
        return dict(slots)

    async def change_status_schedule(self, doctor, is_available, schedule_id):
        doctor = await self.user_repo.find_one(id=doctor.id)
        if not doctor:
            raise NotFoundUserByIDException()

        schedule = await self.doctor_schedule_repo.find_one(id=schedule_id)
        if schedule.doctor_id != doctor.id:
            raise ThisIsNotYoursScheduleException().message

        await self.doctor_schedule_repo.schedule_change_status(schedule_id=schedule_id, status=is_available)
        return 'Изменен статус слота'

    async def show_all_schedules_doctors(self, doctor_id: int, day_of_week: str, start_time: time, end_time: time):
        if not await self.user_repo.find_one(id=doctor_id, role='doctor'):
            raise YouAreNotDoctorException().message

        filters = {
            "doctor_id": doctor_id,
            "day_of_week": day_of_week,
            "is_available": True,
        }

        if start_time and end_time:
            filters["start_time"] = start_time
            filters["end_time"] = end_time

        slots = await self.doctor_schedule_repo.find_all_by_filters(**filters)
        formatted_schedule = format_schedule(slots)
        return {"Свободные слоты": formatted_schedule}

    async def show_all_appointments(self, user_id: int):
        appointments = await self.appointment_repo.find_all_by_filters(patient_id=user_id)
        return await self.format_appointment(appointments)

    async def create_appointment(self, doctor_data, user_id):
        schedule = await self.doctor_schedule_repo.find_one(id=doctor_data.schedule_id)
        user = await self.user_repo.find_one(id=user_id)
        doctor = await self.user_repo.find_one(id=doctor_data.doctor_id, role='doctor')
        date_today = datetime.date.today()

        if not schedule:
            raise NotFoundScheduleException().message
        if not schedule.is_available:
            raise SlotIsOccupiedException().message

        if not await self.user_repo.find_one(id=doctor_data.doctor_id):
            raise NotFoundDoctorOrUserIsNotDoctorException().message

        if doctor_data.doctor_id != schedule.doctor_id:
            raise ThisIsAnotherDoctorException().message

        exists_appointment = await self.appointment_repo.find_one(
            doctor_id=doctor_data.doctor_id,
            patient_id=user.id,
            schedule_id=doctor_data.schedule_id,
        )
        if exists_appointment or exists_appointment.date == date_today:
            raise AppointmentAlreadyExistsException().message

        await self.appointment_repo.add(
            doctor_id=doctor_data.doctor_id,
            patient_id=user.id,
            schedule_id=doctor_data.schedule_id,
            date=doctor_data.date_appointment,
            status="ожидание",
        )
        appointment = await self.appointment_repo.find_one(
            doctor_id=doctor_data.doctor_id,
            patient_id=user.id,
            schedule_id=doctor_data.schedule_id,
            status="ожидание",
        )

        token = create_url_safe_token({'email': user.email, 'appointment_id': appointment.id})
        link = f"http://{settings.DOMAIN}/auth/verify/{token}"
        message = f"""
            Привет! Ты отправил запрос на запись к врачу {doctor.full_name}
            Чтобы подтвердить запись, перейди по этой ссылке: {link}
        """
        send_confirmation_email.delay(patient_email=user.email, message=message)
        return f'Создана новая запись, мы отправили вам на почту ссылку на подтверждение записи к {doctor.full_name}'

    async def my_appointments(self, doctor_id):
        doctor = await self.user_repo.find_one(id=doctor_id, role='doctor')
        if not doctor:
            raise NotFoundDoctorOrUserIsNotDoctorException().message

        appointments = await self.appointment_repo.find_all_by_filters(doctor_id=doctor_id, status='ожидание')
        return appointments

    async def cancel_appointment(self, user_id, appointment_id):
        appointment = await self.appointment_repo.find_one(id=appointment_id, patient_id=user_id, status='ожидание')
        if not appointment:
            raise NotFoundAppointmentException().message
        await self.appointment_repo.cancel_appointment(appointment_id)
        return 'Запись отменена'
