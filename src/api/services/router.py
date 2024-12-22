from typing import Annotated

from fastapi import APIRouter, Depends

from src.api.services.dependencies import services_service
from src.schemas.services import SServiceRequest
from src.services.auth_service import get_current_user
from src.services.service_service import ServicesService

router = APIRouter(prefix='/services', tags=['Услуги'])


@router.post('/create-service')
async def create_service_endpoint(
    service_data: SServiceRequest,
    services: Annotated[ServicesService, Depends(services_service)],
    user: str = Depends(get_current_user),
):
    return await services.create_service(user=user, service_data=service_data)
