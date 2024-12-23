from fastapi import FastAPI

from src.api.auth.router import router as auth_router
from src.api.doctors.router import router as doctor_router
from src.api.patients.router import router as patient_router
from src.api.search.router import router as search_router
from src.api.services.router import router as service_router
from src.api.wallet.router import router as wallet_router

app = FastAPI(docs_url="/docs", description="Приложение для записи к врачу и назначения диагноза")
app.include_router(patient_router)
app.include_router(doctor_router)
app.include_router(auth_router)
app.include_router(wallet_router)
app.include_router(service_router)
app.include_router(search_router)
