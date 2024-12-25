from dataclasses import dataclass
from datetime import date

from src.exceptions.auth.user import NotFoundUserException
from src.exceptions.medical_card.card import NotFoundMedicalCardException
from src.repos.base import BaseRepo


@dataclass
class SearchService:
    user_repo: BaseRepo
    medical_card_repo: BaseRepo
    visits_repo: BaseRepo

    async def format_user(self, user):
        medical_card = await self.medical_card_repo.find_one(patient_id=user.id)
        if not medical_card:
            medical_card_id = None
        else:
            medical_card_id = medical_card.id
        return {
            'ID пользователя': user.id,
            'ФИО': user.full_name,
            'Статус': user.role,
            'Номер телефона': user.phone_number,
            'Почта': user.email,
            'Мед.карта': medical_card_id,
        }

    async def find_by_full_name(self, full_name: str):
        user = await self.user_repo.find_by_full_name(full_name=full_name)
        if not user:
            raise NotFoundUserException().message
        return await self.format_user(user)

    async def find_by_phone_number(self, phone_number: str):
        user = await self.user_repo.find_one(phone_number=phone_number)
        if not user:
            raise NotFoundUserException().message
        return await self.format_user(user)

    async def find_by_medical_card_id(self, medical_card_id: int):
        med_card = await self.medical_card_repo.find_one(id=medical_card_id)
        if not med_card:
            raise NotFoundMedicalCardException().message
        user = await self.user_repo.find_one(id=med_card.patient_id)

        return await self.format_user(user)

    async def filter_visits_to_doctor(self, user_id: int, date: date):
        visit = await self.visits_repo.find_one(visit_date=date, patient_id=user_id)
        return visit
