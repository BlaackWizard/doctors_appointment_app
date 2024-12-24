from typing import Annotated

from fastapi import Depends, FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from src.api.auth.router import router as auth_router
from src.api.doctors.router import router as doctor_router
from src.api.patients.router import router as patient_router
from src.api.report.dependencies import report_services
from src.api.report.router import router as report_router
from src.api.search.router import router as search_router
from src.api.services.router import router as service_router
from src.api.wallet.router import router as wallet_router
from src.services.report_services import ReportServices

app = FastAPI(docs_url="/docs", description="Приложение для записи к врачу и назначения диагноза")

templates = Jinja2Templates(directory='src/templates')


@app.get("/", response_class=HTMLResponse)
async def dashboard(report_services: Annotated[ReportServices, Depends(report_services)], request: Request):
    total_count_users = await report_services.total_count_patient()
    total_count_doctors = await report_services.total_count_doctors()
    total_count_services = await report_services.total_count_services()
    total_count_diagnosis = await report_services.total_count_diagnoses()

    context = {
        "request": request,
        "total_count_users": total_count_users,
        "total_count_doctors": total_count_doctors,
        "total_count_services": total_count_services,
        "total_count_diagnosis": total_count_diagnosis,
    }
    return templates.TemplateResponse("dashboard.html", context)


app.include_router(patient_router)
app.include_router(doctor_router)
app.include_router(auth_router)
app.include_router(wallet_router)
app.include_router(service_router)
app.include_router(search_router)
app.include_router(report_router)
