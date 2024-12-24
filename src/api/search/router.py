from datetime import date
from typing import Annotated

from fastapi import APIRouter, Depends

from src.api.search.dependencies import search_service
from src.services.search import SearchService

router = APIRouter(prefix='/search', tags=['Поисковик'])


@router.get('/by-name/{full_name}')
async def find_by_full_name(
    search_services: Annotated[SearchService, Depends(search_service)],
    full_name: str,
):
    return await search_services.find_by_full_name(full_name)


@router.get("/by-phone/{phone_number}")
async def find_by_phone_number(
    search_services: Annotated[SearchService, Depends(search_service)],
    phone_number: str,
):
    return await search_services.find_by_phone_number(phone_number)


@router.get("/by-id-medical-card/{medical_card}")
async def find_by_medical_card_id(
    search_services: Annotated[SearchService, Depends(search_service)],
    medical_card_id: int,
):
    return await search_services.find_by_medical_card_id(medical_card_id)


@router.get("/by-visit-to-doctor/{visits_to_doctor}")
async def find_by_date_visit_to_doctor(
    search_services: Annotated[SearchService, Depends(search_service)],
    date: date,
    user_id: int,
):
    return await search_services.filter_visits_to_doctor(date=date, user_id=user_id)
