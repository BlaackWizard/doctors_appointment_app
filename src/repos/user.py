from sqlalchemy import select

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
