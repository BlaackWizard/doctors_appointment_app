from collections import defaultdict
from dataclasses import dataclass
from datetime import date, time

from src.exceptions.appointment.doctor import (
    NotFoundDoctorOrUserIsNotDoctorException, ThisIsNotYoursScheduleException)
from src.exceptions.appointment.not_found_schedule import (
    NotFoundScheduleException, SlotIsOccupiedException)
from src.exceptions.auth.user import NotFoundUserByIDException
from src.repos.base import BaseRepo


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

    async def create_schedule(self, doctor, doctor_data):
        doctor = await self.user_repo.find_one(id=doctor.id)
        if not doctor:
            raise NotFoundUserByIDException().message

        schedule = await self.doctor_schedule_repo.add(
            doctor_id=doctor.id,
            day_of_week=doctor_data.day_of_week,
            date=doctor_data.date,
            start_time=doctor_data.start_time,
            end_time=doctor_data.end_time,
        )
        return schedule

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
                "created_at": appointment.date,
            })
        return dict(slots)

    async def change_status_schedule(self, doctor, schedule_id):
        doctor = await self.user_repo.find_one(id=doctor.id)
        if not doctor:
            raise NotFoundUserByIDException()
        schedule = await self.doctor_schedule_repo.find_one(id=schedule_id)
        if schedule.doctor_id != doctor.id:
            raise ThisIsNotYoursScheduleException().message

        await self.doctor_schedule_repo.schedule_is_not_available(schedule_id)

        return 'Изменен статус слота'

    async def show_all_schedules_doctors(self, doctor_id: int, date: date, start_time: time, end_time: time):
        if start_time or end_time is None:

            slots = await self.doctor_schedule_repo.find_all_by_filters(
                doctor_id=doctor_id,
                date=date,
                is_available=True,
            )
        else:
            slots = await self.doctor_schedule_repo.find_all_by_filters(
                doctor_id=doctor_id,
                date=date,
                start_time=start_time,
                end_time=end_time,
                is_available=True,
            )
        formatted_schedule = format_schedule(slots)
        return {"Свободные слоты": formatted_schedule}

    async def show_all_appointments(self, user_id: int):
        appointments = await self.appointment_repo.find_all_by_filters(patient_id=user_id)
        return await self.format_appointment(appointments)

    async def create_appointment(self, doctor_data, user_id):
        schedule = await self.doctor_schedule_repo.find_one(id=doctor_data.schedule_id)
        if not schedule:
            raise NotFoundScheduleException().message
        if not schedule.is_available:
            raise SlotIsOccupiedException().message

        if not await self.user_repo.find_one(id=doctor_data.doctor_id):
            raise NotFoundDoctorOrUserIsNotDoctorException().message

        naive_datetime = doctor_data.date.replace(tzinfo=None)

        await self.appointment_repo.add(
            doctor_id=doctor_data.doctor_id,
            patient_id=user_id,
            schedule_id=doctor_data.schedule_id,
            date=naive_datetime,
        )

        await self.doctor_schedule_repo.schedule_is_not_available(schedule_id=doctor_data.schedule_id)

        return 'Запись успешно создана'
