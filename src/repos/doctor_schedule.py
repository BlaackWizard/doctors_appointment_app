from sqlalchemy import delete, update

from ..db.connect import async_session_maker
from ..models.appointment import AppointmentModel
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

    @classmethod
    async def delete_one(cls, model_id):
        async with async_session_maker() as session:
            await session.execute(
                delete(AppointmentModel).where(AppointmentModel.schedule_id == model_id),
            )
            await session.commit()
            await session.execute(
                delete(cls.model).where(cls.model.id == model_id),
            )
            await session.commit()
