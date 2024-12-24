from dataclasses import dataclass

from src.repos.base import BaseRepo
from src.schemas.services import SServiceRequest, SServiceResponse


@dataclass
class ServicesService:
    service_repo: BaseRepo

    async def create_service(self, service_data: SServiceRequest):
        await self.service_repo.add(
            title=service_data.title,
            cost=service_data.cost,
            requisites=service_data.requisites,
        )
        service = await self.service_repo.find_one(
            title=service_data.title,
            cost=service_data.cost,
            requisites=service_data.requisites,
        )
        return SServiceResponse(
            message="Услуга создана",
            title=service_data.title,
            cost=service_data.cost,
            requisites=service_data.requisites,
            service_id=service.id,
        )
