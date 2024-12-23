from dataclasses import dataclass

from src.exceptions.payment.service import CreateServiceCanOnlyAdminException
from src.repos.base import BaseRepo
from src.schemas.services import SServiceRequest, SServiceResponse


@dataclass
class ServicesService:
    service_repo: BaseRepo

    async def create_service(self, user, service_data: SServiceRequest):
        if user.role != 'admin':
            raise CreateServiceCanOnlyAdminException().message

        await self.service_repo.add(
            title=service_data.title,
            cost=service_data.cost,
            requisites=service_data.requisites,
        )
        return SServiceResponse(
            message="Услуга создана",
            title=service_data.title,
            cost=service_data.cost,
            requisites=service_data.requisites,
        )
