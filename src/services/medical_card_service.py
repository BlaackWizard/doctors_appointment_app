from dataclasses import dataclass
from datetime import date

from src.exceptions.medical_card.card import (
    NotFoundMedicalCardException, ThisIsNotYourMedicalCardException)
from src.exceptions.user.roles import (PatientDoctorConflictException,
                                       ThisUserIsNotDoctorException,
                                       YouAreNotPatientException)
from src.repos.base import BaseRepo
from src.utils.pagination import paginate


@dataclass
class MedicalCardService:
    user_repo: BaseRepo
    medical_card_repo: BaseRepo
    diagnosis_repo: BaseRepo
    visits_repo: BaseRepo
    procedure_repo: BaseRepo
    appointment_repo: BaseRepo
    analyze_repo: BaseRepo

    async def create_medical_card(self, patient_id: int, doctor_id: int, birth_day: date, contacts: str):
        user = await self.user_repo.find_one(id=patient_id)
        doctor = await self.user_repo.find_one(id=doctor_id)

        if user.role != "patient":
            raise YouAreNotPatientException().message

        if not doctor or doctor.role != "doctor":
            raise ThisUserIsNotDoctorException().message

        appointment = await self.appointment_repo.find_one(
            patient_id=patient_id,
            doctor_id=doctor_id,
            status='подтверждено',
        )
        if not appointment:
            raise PatientDoctorConflictException().message

        await self.medical_card_repo.add(
            patient_id=patient_id,
            doctor_id=doctor_id,
            doctor_fullname=doctor.full_name,
            patient_fullname=user.full_name,
            birth_day=birth_day,
            contacts=contacts,
        )
        medical_card = await self.medical_card_repo.find_one(
            patient_id=patient_id,
            doctor_id=doctor_id,
        )
        return medical_card

    async def get_medical_card(self, user_id: int, page: int = 1, limit: int = 10):
        medical_card = await self.medical_card_repo.find_one(patient_id=user_id)
        if not medical_card:
            raise NotFoundMedicalCardException().message

        if user_id != medical_card.patient_id:
            raise ThisIsNotYourMedicalCardException().message

        diagnoses = await paginate(
            self.diagnosis_repo.find_all_by_filters,
            page,
            limit,
            medical_card_id=medical_card.id,
        )
        visits = await paginate(
            self.visits_repo.find_all_by_filters,
            page,
            limit,
            patient_id=user_id,
        )
        procedures = await paginate(
            self.procedure_repo.find_all_by_filters,
            page,
            limit,
            medical_card_id=medical_card.id,
        )
        analyzes = await paginate(
            self.analyze_repo.find_all_by_filters,
            page,
            limit,
            medical_card_id=medical_card.id,
        )

        return {
            "Медицинская карта": medical_card,
            "Диагнозы": diagnoses,
            "Посещения": visits,
            "Процедуры": procedures,
            'Анализы': analyzes,
        }

    async def change_doctor_in_medical_card(self, user, doctor_id):
        doctor = await self.user_repo.find_one(id=doctor_id, role='doctor')
        medical_card = await self.medical_card_repo.find_one(patient_id=user.id)

        if not medical_card:
            raise NotFoundMedicalCardException().message

        if not doctor:
            raise ThisUserIsNotDoctorException().message

        await self.medical_card_repo.change_doctor(medical_card_id=medical_card.id, doctor_id=doctor_id)

        return 'Успешно поменялся врач в мед.карте'
