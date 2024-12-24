from sqlalchemy import func, select

from src.db.connect import async_session_maker
from src.models.services import Services
from src.repos.sqlalchemy import SQLAlchemyRepo


class ServiceRepo(SQLAlchemyRepo):
    model = Services

    @classmethod
    async def total_count_services(cls):
        async with async_session_maker() as session:
            query = select(func.count(cls.model.id))
            result = await session.execute(query)
            return result.scalar()
