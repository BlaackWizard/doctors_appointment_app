from dataclasses import dataclass

from src.exceptions.medical_card.card import (
    NotFoundMedicalCardException, ThisIsNotYourMedicalCardException,
    YouAreNotDoctorException, YouAreNotPatientException)
from src.repos.base import BaseRepo
from src.schemas.medical_card import SDiagnosis


@dataclass
class MedicalCardService:
    user_repo: BaseRepo
    medical_card_repo: BaseRepo
    diagnosis_repo: BaseRepo
    visits_repo: BaseRepo

    async def create_medical_card(self, patient_id: int, doctor_id: int):
        user = await self.user_repo.find_one(id=patient_id)
        doctor = await self.user_repo.find_one(id=doctor_id)

        if user.role != "patient":
            raise YouAreNotPatientException().message

        if not doctor or doctor.role != "doctor":
            raise YouAreNotDoctorException().message

        await self.medical_card_repo.add(
            patient_id=patient_id,
            doctor_id=doctor_id,
            doctor_fullname=doctor.full_name,
            patient_fullname=user.full_name,
        )
        return 'Создана медицинская карта!'

    async def get_medical_card(self, user_id: int):
        medical_card = await self.medical_card_repo.find_one(patient_id=user_id)
        if not medical_card:
            raise NotFoundMedicalCardException().message

        if user_id != medical_card.patient_id:
            raise ThisIsNotYourMedicalCardException().message

        diagnoses = await self.diagnosis_repo.find_all_by_filters(medical_card_id=medical_card.id)
        visits = await self.visits_repo.find_all_by_filters(medical_card_id=medical_card.id)

        return {
            "Медицинская карта": medical_card,
            "Диагнозы": diagnoses,
            "Посещения": visits,
        }


@dataclass
class DiagnoseService:
    medical_card_repo: BaseRepo
    diagnosis_repo: BaseRepo

    async def create_diagnose(self, doctor_id: int, diagnose_data: SDiagnosis):
        medical_card = await self.medical_card_repo.find_one(id=diagnose_data.medical_card_id)
        if not medical_card:
            raise NotFoundMedicalCardException().message

        if doctor_id != medical_card.doctor_id:
            raise ThisIsNotYourMedicalCardException().message

        await self.diagnosis_repo.add(
            diagnosis_text=diagnose_data.diagnosis_text,
            recommendation=diagnose_data.recommendation,
            medical_card_id=diagnose_data.medical_card_id,
            date=diagnose_data.date,
        )
        return 'Диагноз успешно создан'


@dataclass
class VisitService:
    medical_repo: BaseRepo
    visits_repo: BaseRepo

    async def create_visit(self, doctor_id: int, visit_data):
        medical_card = await self.medical_repo.find_one(id=visit_data.medical_card_id)
        if not medical_card:
            raise NotFoundMedicalCardException().message

        if doctor_id != medical_card.doctor_id:
            raise ThisIsNotYourMedicalCardException().message

        await self.visits_repo.add(
            visit_date=visit_data.visit_date,
            doctor_name=visit_data.doctor_name,
            notes=visit_data.notes,
            medical_card_id=visit_data.medical_card_id,
        )
        return 'Посещение успешно создано'
