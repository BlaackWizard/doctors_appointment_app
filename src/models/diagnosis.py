from sqlalchemy import Column, Date, ForeignKey, Integer, Text
from sqlalchemy.orm import relationship

from src.db.connect import Base


class Diagnosis(Base):
    __tablename__ = "diagnosis"

    id = Column(Integer, primary_key=True) # noqa
    diagnosis_text = Column(Text)
    recommendation = Column(Text)
    medical_card_id = Column(Integer, ForeignKey('medical_cards.id'))
    date = Column(Date)

    medical_card = relationship("MedicalCardModel", back_populates="diagnosis")
