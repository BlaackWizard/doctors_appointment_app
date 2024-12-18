from collections import defaultdict
from dataclasses import dataclass

from src.exceptions.appointment.doctor import ThisIsNotYoursScheduleException
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
            start_time=doctor_data.start_time,
            end_time=doctor_data.end_time,
        )
        return schedule

    async def change_status_schedule(self, doctor, schedule_id):
        doctor = await self.user_repo.find_one(id=doctor.id)
        if not doctor:
            raise NotFoundUserByIDException()
        schedule = await self.doctor_schedule_repo.find_one(id=schedule_id)
        if schedule.doctor_id != doctor.id:
            raise ThisIsNotYoursScheduleException().message

        await self.doctor_schedule_repo.schedule_is_not_available(schedule_id)

        return 'Изменен статус слота'

    async def show_all_schedules_doctors(self, doctor_id: int):
        slots = await self.doctor_schedule_repo.find_all_by_filters(doctor_id=doctor_id)
        formatted_schedule = format_schedule(slots)
        return {"Расписание": formatted_schedule}

    async def create_appointment(self, doctor_data):
        schedule = await self.doctor_schedule_repo.find_one(id=doctor_data.schedule_id)
        if not schedule:
            raise NotFoundScheduleException().message
        if not schedule.is_avaible():
            raise SlotIsOccupiedException().message

        appointment = await self.appointment_repo.add(
            doctor_id=doctor_data.doctor_id,
            patient_id=doctor_data.patient_id,
            schedule_id=doctor_data.schedule_id,
        )
        await self.doctor_schedule_repo.schedule_is_not_available(schedule_id=appointment.schedule_id)
        return appointment
