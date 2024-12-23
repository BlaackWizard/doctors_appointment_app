from src.repos.services import ServiceRepo
from src.services.service_service import ServicesService


def services_service():
    return ServicesService(
        service_repo=ServiceRepo,
    )
