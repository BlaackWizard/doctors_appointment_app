from dataclasses import dataclass

from src.exceptions.auth.user import UserNotPatientException
from src.exceptions.medical_card.visit import \
    BeforeCreateVisitPatientMustCreateAppointmentException
from src.exceptions.user.roles import YouAreNotDoctorException
from src.repos.base import BaseRepo


@dataclass
class VisitService:
    user_repo: BaseRepo
    visits_repo: BaseRepo
    appointment_repo: BaseRepo
    medical_card_repo: BaseRepo

    async def create_visit(self, doctor_id: int, visit_data):
        patient = await self.user_repo.find_one(id=visit_data.patient_id)
        doctor = await self.user_repo.find_one(id=doctor_id)

        if not patient or patient.role != 'patient':
            raise UserNotPatientException().message

        if not doctor or doctor.role != 'doctor':
            raise YouAreNotDoctorException().message

        appointment = await self.appointment_repo.find_one(
            doctor_id=doctor_id,
            patient_id=visit_data.patient_id,
            status='ожидание',
        )

        if not appointment:
            raise BeforeCreateVisitPatientMustCreateAppointmentException().message

        medical_card = await self.medical_card_repo.find_one(patient_id=patient.id)
        if medical_card:
            await self.visits_repo.add(
                visit_date=visit_data.visit_date,
                doctor_id=doctor_id,
                patient_id=visit_data.patient_id,
                medical_card_id=medical_card.id,
            )
        await self.visits_repo.add(
            visit_date=visit_data.visit_date,
            doctor_id=doctor_id,
            patient_id=visit_data.patient_id,
        )

        await self.appointment_repo.update_status(appointment_id=appointment.id, status='подтверждено')

        return 'Посещение успешно создано'
