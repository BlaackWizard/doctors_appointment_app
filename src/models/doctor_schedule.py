from sqlalchemy import Boolean, Column, Date, ForeignKey, Integer, String, Time
from sqlalchemy.orm import relationship

from src.db.connect import Base


class DoctorScheduleModel(Base):
    __tablename__ = "doctor_schedule"

    id = Column(Integer, primary_key=True)  # noqa
    doctor_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    day_of_week = Column(String, nullable=True)
    date = Column(Date, nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    is_available = Column(Boolean, default=True)

    doctor = relationship("UserModel", back_populates="schedules")
