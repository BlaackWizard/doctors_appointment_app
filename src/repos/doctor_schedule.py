from sqlalchemy import update

from ..db.connect import async_session_maker
from ..models.doctor_schedule import DoctorScheduleModel
from .sqlalchemy import SQLAlchemyRepo


class DoctorScheduleRepo(SQLAlchemyRepo):
    model = DoctorScheduleModel

    @classmethod
    async def schedule_is_not_available(cls, schedule_id):
        async with async_session_maker() as session:
            query = update(cls.model).where(cls.model.id == schedule_id).values(is_available=False)
            await session.execute(query)
            await session.commit()
