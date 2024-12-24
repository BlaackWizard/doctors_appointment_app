from dataclasses import dataclass

from src.repos.base import BaseRepo


@dataclass
class ReportServices:
    appointment_repo: BaseRepo
    payment_repo: BaseRepo
    user_repo: BaseRepo
    services_repo: BaseRepo
    diagnoses_repo: BaseRepo

    async def count_all_appointment(self):
        return await self.appointment_repo.count()

    async def financial_receipts(self, year: int):
        return await self.payment_repo.get_monthly_financial_report(
            year=year,
        )

    async def count_patients(self, year: int):
        return await self.user_repo.count_patients(year)

    async def total_count_patient(self):
        return await self.user_repo.total_count_patients()

    async def total_count_doctors(self):
        return await self.user_repo.total_count_doctors()

    async def total_count_services(self):
        return await self.services_repo.total_count_services()

    async def total_count_diagnoses(self):
        return await self.diagnoses_repo.total_count_diagnoses()
