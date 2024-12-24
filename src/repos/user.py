from sqlalchemy import extract, func, select

from ..db.connect import async_session_maker
from ..models.user import UserModel
from .sqlalchemy import SQLAlchemyRepo


class UserRepo(SQLAlchemyRepo):
    model = UserModel

    @classmethod
    async def find_by_full_name(cls, full_name: str):
        async with async_session_maker() as session:
            query = select(cls.model).where(cls.model.full_name.ilike(f"%{full_name}%"))
            result = await session.execute(query)

            return result.scalar_one_or_none()

    @classmethod
    async def count_patients(cls, year: int):
        async with async_session_maker() as session:
            query = (
                select(
                    extract('month', cls.model.date).label("month"),
                    func.count(cls.model.id).label("monthly_count_users"),
                )
                .filter(extract('year', cls.model.date) == year)
                .group_by(extract('month', cls.model.date))
                .order_by(extract('month', cls.model.date)).filter_by(role='patient')
            )
            result = await session.execute(query)

            data = [{"month": int(row[0]), "monthly_count_users": row[1]} for row in result.fetchall()]
            return data

    @classmethod
    async def total_count_patients(cls):
        async with async_session_maker() as session:
            query = (
                select(func.count(cls.model.id))
                .where(cls.model.role == 'patient')
            )
            result = await session.execute(query)
            total_patients = result.scalar()
            return total_patients

    @classmethod
    async def total_count_doctors(cls):
        async with async_session_maker() as session:
            query = (
                select(func.count(cls.model.id))
                .where(cls.model.role == 'doctor')
            )
            result = await session.execute(query)
            total_doctors = result.scalar()
            return total_doctors
