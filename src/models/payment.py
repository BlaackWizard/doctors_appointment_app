from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer
from sqlalchemy.orm import relationship

from src.db.connect import Base


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True) # noqa

    patient_id = Column(Integer, ForeignKey("users.id"))
    service_id = Column(Integer, ForeignKey("services.id"))
    amount = Column(Float)
    date = Column(DateTime, default=datetime.now())
    is_paid = Column(Boolean, default=False)

    patient = relationship("UserModel", back_populates="payment_patient", foreign_keys=[patient_id])
    service = relationship("Services", back_populates="payment", foreign_keys=[service_id])

    def __str__(self):
        return f'Платеж #{self.id}'
