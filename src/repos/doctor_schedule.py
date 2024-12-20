from sqlalchemy import update

from ..db.connect import async_session_maker
from ..models.doctor_schedule import DoctorScheduleModel
from .sqlalchemy import SQLAlchemyRepo


class DoctorScheduleRepo(SQLAlchemyRepo):
    model = DoctorScheduleModel

    @classmethod
    async def schedule_change_status(cls, schedule_id: int, status: bool):
        async with async_session_maker() as session:
            query = update(cls.model).where(cls.model.id == schedule_id).values(is_available=status)
            await session.execute(query)
            await session.commit()
