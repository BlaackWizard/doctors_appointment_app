from fastapi import FastAPI
from src.api.patients.router import router as patient_router

app = FastAPI(docs_url="/docs", description="Приложение для записи к врачу и назначения диагноза")
app.include_router(patient_router)

