from sqlalchemy import Boolean, Column, DateTime, Enum, ForeignKey, Integer
from sqlalchemy.orm import relationship

from src.db.connect import Base


class AppointmentModel(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True) # noqa
    doctor_id = Column(Integer, ForeignKey("users.id"))
    schedule_id = Column(Integer, ForeignKey("doctor_schedule.id"))
    patient_id = Column(Integer, ForeignKey("users.id"))

    date = Column(DateTime, nullable=False)
    status = Column(Enum('ожидание', 'подтверждено', 'отменено', name="appointment_status"), nullable=False)
    is_verified = Column(Boolean, default=False)

    doctor = relationship("UserModel", back_populates="appointment_with_doctor", foreign_keys=[doctor_id])
    patient = relationship("UserModel", back_populates="appointment_with_patient", foreign_keys=[patient_id])

    def __str__(self):
        return f"Запись #{self.id}"
