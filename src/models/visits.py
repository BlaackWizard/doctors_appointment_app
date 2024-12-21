from sqlalchemy import Column, Date, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from src.db.connect import Base


class Visits(Base):
    __tablename__ = "visits"

    id = Column(Integer, primary_key=True)  # noqa
    visit_date = Column(Date)
    doctor_name = Column(String)
    notes = Column(Text)
    patient_id = Column(Integer, ForeignKey("users.id"))
    medical_card_id = Column(Integer, ForeignKey("medical_cards.id"), nullable=True)

    medical_card = relationship("MedicalCardModel", back_populates="visits")
