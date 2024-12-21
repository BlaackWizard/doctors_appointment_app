from dataclasses import dataclass
from datetime import date

from src.exceptions.medical_card.card import NotFoundMedicalCardException, ThisIsNotYourMedicalCardException
from src.exceptions.medical_card.diagnose import NotFoundDiagnoseException, \
    DiagnoseMedicalCardIsDifferentWithUsersMedicalCardException
from src.repos.base import BaseRepo
from src.schemas.medical_card import SDiagnosis


@dataclass
class DiagnoseService:
    medical_card_repo: BaseRepo
    diagnosis_repo: BaseRepo

    async def create_diagnose(self, doctor_id: int, diagnose_data: SDiagnosis):
        medical_card = await self.medical_card_repo.find_one(patient_id=diagnose_data.patient_id)
        if not medical_card:
            raise NotFoundMedicalCardException().message

        if doctor_id != medical_card.doctor_id:
            raise ThisIsNotYourMedicalCardException().message

        await self.diagnosis_repo.add(
            diagnosis_text=diagnose_data.diagnosis_text,
            recommendation=diagnose_data.recommendation,
            medical_card_id=medical_card.id,
            date=date.today(),
        )
        return 'Диагноз успешно создан'

    async def check_diagnose(self, doctor_id, diagnose_data: SDiagnosis, diagnose_id: int):
        diagnose = await self.diagnosis_repo.find_one(id=diagnose_id)
        if not diagnose:
            raise NotFoundDiagnoseException().message
        medical_card = await self.medical_card_repo.find_one(patient_id=diagnose_data.patient_id)

        if not medical_card:
            raise NotFoundMedicalCardException().message

        if diagnose.medical_card_id != medical_card.id:
            raise DiagnoseMedicalCardIsDifferentWithUsersMedicalCardException().message

        if doctor_id != medical_card.doctor_id:
            raise ThisIsNotYourMedicalCardException().message

        return diagnose.date

    async def update_diagnose(self, doctor_id, diagnose_data: SDiagnosis, diagnose_id: int):
        check = await self.check_diagnose(doctor_id=doctor_id, diagnose_data=diagnose_data, diagnose_id=diagnose_id)
        if check:
            medical_card = await self.medical_card_repo.find_one(patient_id=diagnose_data.patient_id)

            await self.diagnosis_repo.update(
                model_id=diagnose_id,
                diagnosis_text=diagnose_data.diagnosis_text,
                recommendation=diagnose_data.recommendation,
                medical_card_id=medical_card.id,
                date=check,
            )
            return 'Обновлены данные диагноза'
