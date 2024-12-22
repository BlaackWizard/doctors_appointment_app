from sqlalchemy import Column, Date, ForeignKey, Integer, String, Text, Float, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from src.db.connect import Base


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True)

    patient_id = Column(Integer, ForeignKey("users.id"))
    service_id = Column(Integer, ForeignKey("services.id"))
    amount = Column(Float)
    date = Column(DateTime, default=datetime.now())
    is_paid = Column(Boolean, default=False)
