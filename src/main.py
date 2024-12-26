from typing import Annotated

from fastapi import Depends, FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqladmin import Admin

from src.admin.appointment import AppointmentAdmin
from src.admin.auth_admin import authentication_backend
from src.admin.doctor_schedule import DoctorScheduleAdmin
from src.admin.medical_card import MedicalCardAdmin
from src.admin.payment import PaymentAdmin
from src.admin.services import ServicesAdmin
from src.admin.users import UserAdmin
from src.admin.visits import VisitsAdmin
from src.api.auth.router import router as auth_router
from src.api.doctors.router import router as doctor_router
from src.api.patients.router import router as patient_router
from src.api.report.dependencies import report_services
from src.api.report.router import router as report_router
from src.api.search.router import router as search_router
from src.api.services.router import router as service_router
from src.api.wallet.router import router as wallet_router
from src.db.connect import engine
from src.services.report_services import ReportServices

app = FastAPI(docs_url="/docs", description="Приложение для записи к врачу и назначения диагноза")
admin = Admin(app, engine, authentication_backend=authentication_backend)


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

admin.add_view(UserAdmin)
admin.add_view(AppointmentAdmin)
admin.add_view(ServicesAdmin)
admin.add_view(PaymentAdmin)
admin.add_view(DoctorScheduleAdmin)
admin.add_view(VisitsAdmin)
admin.add_view(MedicalCardAdmin)
