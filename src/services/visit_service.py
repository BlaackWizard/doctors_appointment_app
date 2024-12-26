from dataclasses import dataclass

from src.repos.base import BaseRepo


@dataclass
class VisitService:
    user_repo: BaseRepo
    appointment_repo: BaseRepo
    medical_card_repo: BaseRepo
    visits_repo: BaseRepo

    async def create_visit(self, visit_data):
        appointment = await self.appointment_repo.find_one(id=visit_data.appointment_id, is_verified=True)

        medical_card = await self.medical_card_repo.find_one(patient_id=appointment.patient_id)
        if medical_card:
            await self.visits_repo.add(
                visit_date=visit_data.visit_date,
                doctor_id=appointment.doctor_id,
                patient_id=appointment.patient_id,
                medical_card_id=medical_card.id,
            )
        await self.visits_repo.add(
            visit_date=visit_data.visit_date,
            doctor_id=appointment.doctor_id,
            patient_id=appointment.patient_id,
        )

        await self.appointment_repo.update_status(appointment_id=appointment.id, status='подтверждено')

        return 'Посещение успешно создано'
