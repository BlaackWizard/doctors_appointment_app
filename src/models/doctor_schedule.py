from sqlalchemy import Column, Integer, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship

from src.db.connect import Base


class DoctorScheduleModel(Base):
    __tablename__ = "doctor_schedule"

    id = Column(Integer, primary_key=True)
    doctor_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    date = Column(DateTime, nullable=False)
    is_available = Column(Boolean, default=True)

    doctor = relationship("UserModel", back_populates="schedules")

