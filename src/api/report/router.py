from typing import Annotated

from fastapi import APIRouter, Depends

from src.services.report_services import ReportServices

from .dependencies import report_services

router = APIRouter(prefix='/reports', tags=['Отчёт и анализ'])


@router.post('/count-appointments-to-doctor')
async def count_appointments_to_doctor_endpoint(
    report_services: Annotated[ReportServices, Depends(report_services)],
):
    return await report_services.count_all_appointment()


@router.get('/financial-receipts/{year}')
async def get_financial_receipts_endpoint(
    report_services: Annotated[ReportServices, Depends(report_services)],
    year: int,
):
    return await report_services.financial_receipts(year=year)


@router.get('/count-users/{year}')
async def get_count_users_for_year(
    report_services: Annotated[ReportServices, Depends(report_services)],
    year: int,
):
    return await report_services.count_patients(year)


@router.get('/total-count-users/{year}')
async def total_count_users_for_year(
    report_services: Annotated[ReportServices, Depends(report_services)],
    year: int,
):
    return await report_services.total_count_patient(year)
