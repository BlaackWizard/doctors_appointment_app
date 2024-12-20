from sqlalchemy import update

from src.db.connect import async_session_maker
from src.models.medical_card import (Diagnosis, MedicalCardModel, Procedure,
                                     Test, Visits)
from src.repos.sqlalchemy import SQLAlchemyRepo


class MedicalCardRepo(SQLAlchemyRepo):
    model = MedicalCardModel

    @classmethod
    async def change_doctor(cls, doctor_id, medical_card_id):
        async with async_session_maker() as session:
            query = update(cls.model).where(cls.model.id == medical_card_id).values(doctor_id=doctor_id)
            await session.execute(query)
            await session.commit()


class VisitsRepo(SQLAlchemyRepo):
    model = Visits


class DiagnosisRepo(SQLAlchemyRepo):
    model = Diagnosis


class TestsRepo(SQLAlchemyRepo):
    model = Test


class ProcedureRepo(SQLAlchemyRepo):
    model = Procedure
