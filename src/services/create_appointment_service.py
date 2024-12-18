from dataclasses import dataclass

from src.exceptions.appointment.not_found_schedule import NotFoundScheduleException, SlotIsOccupiedException
from src.exceptions.auth.not_found_user import NotFoundUserByIDException
from src.repos.base import BaseRepo


@dataclass
class AppointmentService:
    doctor_schedule_repo: BaseRepo
    appointment_repo: BaseRepo
    user_repo: BaseRepo

    async def create_schedule(self, doctor_data):
        doctor = await self.user_repo.find_one(id=doctor_data.doctor_id, role='doctor')
        if not doctor:
            raise NotFoundUserByIDException()

        schedule = await self.doctor_schedule_repo.add(doctor_id=doctor_data.doctor_id, date=doctor_data.date)
        return schedule

    async def create_appointment(self, doctor_data):
        schedule = await self.doctor_schedule_repo.find_one(id=doctor_data.schedule_id)
        if not schedule:
            raise NotFoundScheduleException()
        if not schedule.is_avaible():
            raise SlotIsOccupiedException()

        appointment = await self.appointment_repo.add(
            doctor_id=doctor_data.doctor_id,
            patient_id=doctor_data.patient_id,
            schedule_id=doctor_data.schedule_id
        )
        await self.doctor_schedule_repo.schedule_is_not_available(schedule_id=appointment.schedule_id)
        return appointment
