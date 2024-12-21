from dataclasses import dataclass
from datetime import date

from src.exceptions.auth.user import UserNotPatientException
from src.exceptions.medical_card.card import (
    NotFoundMedicalCardException, ThisIsNotYourMedicalCardException)
from src.exceptions.medical_card.procedure import (
    NotFoundProcedureException,
    ProcedureMedicalCardIsDifferentWithUserMedicalCardException,
    ThisIsNotYourProcedureException)
from src.repos.base import BaseRepo


@dataclass
class AnalyzeService:
    test_repo: BaseRepo
    procedure_repo: BaseRepo
    medical_card_repo: BaseRepo
    user_repo: BaseRepo

    async def create_procedure(self, user_id: int, doctor, procedure_data):
        user = await self.user_repo.find_one(id=user_id)

        if user.role != 'patient':
            raise UserNotPatientException().message

        medical_card = await self.medical_card_repo.find_one(patient_id=user.id)
        if not medical_card:
            raise NotFoundMedicalCardException().message

        if user_id != medical_card.patient_id:
            raise ThisIsNotYourMedicalCardException().message

        if doctor.id != medical_card.doctor_id:
            raise ThisIsNotYourMedicalCardException().message

        await self.procedure_repo.add(
            procedure_name=procedure_data.procedure_name,
            description=procedure_data.description,
            date=date.today(),
            doctor_id=doctor.id,
            doctor_fullname=doctor.full_name,
            medical_card_id=medical_card.id,
        )
        return 'Анализы успешно созданы'

    async def check_procedure(self, user_id: int, doctor_id: int, procedure_id):
        procedure = await self.procedure_repo.find_one(id=procedure_id)

        if not procedure:
            raise NotFoundProcedureException().message

        user = await self.user_repo.find_one(id=user_id, role='patient')

        if not user:
            raise UserNotPatientException().message

        medical_card = await self.medical_card_repo.find_one(patient_id=user.id)

        if doctor_id != procedure.doctor_id:
            raise ThisIsNotYourProcedureException().message

        if not medical_card:
            raise NotFoundMedicalCardException().message

        if procedure.medical_card_id != medical_card.id:
            raise ProcedureMedicalCardIsDifferentWithUserMedicalCardException().message

        return procedure.date

    async def update_procedure(self, user_id: int, doctor, procedure_data, procedure_id: int):
        check = await self.check_procedure(user_id=user_id, doctor_id=doctor.id, procedure_id=procedure_id)
        if check:

            medical_card = await self.medical_card_repo.find_one(patient_id=user_id)

            await self.procedure_repo.update(
                model_id=procedure_id,
                procedure_name=procedure_data.procedure_name,
                description=procedure_data.description,
                date=check,
                doctor_id=doctor.id,
                doctor_fullname=doctor.full_name,
                medical_card_id=medical_card.id,
            )
            return 'Обновлены данные процедуры'
