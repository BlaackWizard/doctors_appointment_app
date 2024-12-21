from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from src.db.connect import Base


class Analyzes(Base):
    __tablename__ = "analyzes"

    id = Column(Integer, primary_key=True, index=True) # noqa
    analyze_name = Column(String)
    result = Column(Text)
    file = Column(String)
    medical_card_id = Column(Integer, ForeignKey('medical_cards.id'))

    medical_card = relationship("MedicalCardModel", back_populates="analyzes")
