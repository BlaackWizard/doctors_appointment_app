from sqlalchemy import extract, func, select

from ..db.connect import async_session_maker
from ..exceptions.user.user import MultipleResultsFoundException
from ..models.user import UserModel
from .sqlalchemy import SQLAlchemyRepo


class UserRepo(SQLAlchemyRepo):
    model = UserModel

    @classmethod
    async def find_by_full_name(cls, full_name: str):
        async with async_session_maker() as session:
            query = select(cls.model).where(cls.model.full_name.ilike(f"%{full_name}%"))
            result = await session.execute(query)
            records = result.scalars().all()

            if len(records) > 1:
                raise MultipleResultsFoundException().message

            return records[0] if records else None

    @classmethod
    async def count_patients(cls, year: int):
        async with async_session_maker() as session:
            query = (
                select(
                    extract('month', cls.model.date).label("month"),
                    func.count(cls.model.id).label("monthly_count_users"),
                )
                .filter(
                    extract('year', cls.model.date) == year,
                    cls.model.role == 'patient',
                )
                .group_by(extract('month', cls.model.date))
                .order_by(extract('month', cls.model.date))
            )
            result = await session.execute(query)
            return [
                {"month": int(row[0]), "monthly_count_users": row[1]}
                for row in result.fetchall()
            ]

    @classmethod
    async def total_count_by_role(cls, role: str):
        async with async_session_maker() as session:
            query = select(func.count(cls.model.id)).where(cls.model.role == role)
            result = await session.execute(query)
            return result.scalar()

    @classmethod
    async def total_count_patients(cls):
        return await cls.total_count_by_role('patient')

    @classmethod
    async def total_count_doctors(cls):
        return await cls.total_count_by_role('doctor')
