from dataclasses import dataclass
from datetime import date

from src.repos.base import BaseRepo


@dataclass
class SearchService:
    user_repo: BaseRepo
    medical_card_repo: BaseRepo
    visits_repo: BaseRepo

    async def find_by_full_name(self, full_name: str):
        user = await self.user_repo.find_by_full_name(full_name=full_name)
        return user

    async def find_by_phone_number(self, phone_number: str):
        user = await self.user_repo.find_one(phone_number=phone_number)
        return user

    async def find_by_medical_card_id(self, medical_card_id: int):
        med_card = await self.medical_card_repo.find_one(id=medical_card_id)
        user = await self.user_repo.find_one(id=med_card.patient_id)
        return user

    async def filter_visits_to_doctor(self, user_id: int, date: date):
        visit = await self.visits_repo.find_one(visit_date=date, patient_id=user_id)
        return visit
