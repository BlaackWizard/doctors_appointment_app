from sqlalchemy import Column, Integer, ForeignKey, DateTime, String, Enum
from sqlalchemy.orm import relationship

from src.db.connect import Base

class AppointmentModel(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True)
    doctor_id = Column(Integer, ForeignKey("users.id"))
    schedule_id = Column(Integer, ForeignKey("doctor_schedule.id"))
    patient_id = Column(Integer, ForeignKey("users.id"))

    date = Column(DateTime)
    status = Column(Enum('ожидание', 'подтверждено', 'отменено', name="appointment_status"))

    doctor = relationship("User", foreign_keys=[doctor_id])
    patient = relationship("User", foreign_keys=[patient_id])
