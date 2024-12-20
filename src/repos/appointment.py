from sqlalchemy import update

from ..db.connect import async_session_maker
from ..models.appointment import AppointmentModel
from .sqlalchemy import SQLAlchemyRepo


class AppointmentRepo(SQLAlchemyRepo):
    model = AppointmentModel

    @classmethod
    async def update_status(cls, appointment_id: int, status: str):
        async with async_session_maker() as session:
            query = update(cls.model).where(cls.model.id == appointment_id).values(status=status)
            await session.execute(query)
            await session.commit()
