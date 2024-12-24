from sqlalchemy import func, select, update

from src.db.connect import async_session_maker
from src.models.analyzes import Analyzes
from src.models.diagnosis import Diagnosis
from src.models.medical_card import MedicalCardModel
from src.models.procedure import Procedure
from src.models.visits import Visits
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

    @classmethod
    async def find_all_by_filters(cls, limit: int, offset: int, patient_id: int):
        async with async_session_maker() as session:
            query = select(cls.model).filter(cls.model.patient_id == patient_id)
            result = await session.execute(query.offset(offset).limit(limit))
            return result.scalars().all()


class DiagnosisRepo(SQLAlchemyRepo):
    model = Diagnosis

    @classmethod
    async def total_count_diagnoses(cls):
        async with async_session_maker() as session:
            query = select(func.count(cls.model.id))
            result = await session.execute(query)
            return result.scalar()

    @classmethod
    async def find_all_by_filters(cls, limit: int, offset: int, medical_card_id: int):
        async with async_session_maker() as session:
            query = select(cls.model).filter(cls.model.medical_card_id == medical_card_id)
            result = await session.execute(query.offset(offset).limit(limit))
            return result.scalars().all()


class AnalyzeRepo(SQLAlchemyRepo):
    model = Analyzes

    @classmethod
    async def find_all_by_filters(cls, limit: int, offset: int, medical_card_id: int):
        async with async_session_maker() as session:
            query = select(cls.model).filter(cls.model.medical_card_id == medical_card_id)
            result = await session.execute(query.offset(offset).limit(limit))
            return result.scalars().all()


class ProcedureRepo(SQLAlchemyRepo):
    model = Procedure

    @classmethod
    async def find_all_by_filters(cls, limit: int, offset: int, medical_card_id: int):
        async with async_session_maker() as session:
            query = select(cls.model).filter(cls.model.medical_card_id == medical_card_id)
            result = await session.execute(query.offset(offset).limit(limit))
            return result.scalars().all()
