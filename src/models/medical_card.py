from sqlalchemy import Column, Date, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from src.db.connect import Base


class MedicalCardModel(Base):
    __tablename__ = "medical_cards"

    id = Column(Integer, primary_key=True)  # noqa
    patient_id = Column(Integer, ForeignKey('users.id'))
    doctor_id = Column(Integer, ForeignKey('users.id'))
    doctor_fullname = Column(String, nullable=False)
    patient_fullname = Column(String, nullable=False)
    birth_day = Column(Date, nullable=False)
    contacts = Column(String, nullable=False)

    visits = relationship("Visits", back_populates="medical_card")
    diagnosis = relationship("Diagnosis", back_populates="medical_card")
    tests = relationship("Test", back_populates="medical_card")
    procedures = relationship("Procedure", back_populates="medical_card")


class Visits(Base):
    __tablename__ = "visits"

    id = Column(Integer, primary_key=True)  # noqa
    visit_date = Column(Date)
    doctor_name = Column(String)
    notes = Column(Text)
    patient_id = Column(Integer, ForeignKey("users.id"))
    medical_card_id = Column(Integer, ForeignKey("medical_cards.id"), nullable=True)

    medical_card = relationship("MedicalCardModel", back_populates="visits")


class Diagnosis(Base):
    __tablename__ = "diagnosis"

    id = Column(Integer, primary_key=True) # noqa
    diagnosis_text = Column(Text)
    recommendation = Column(Text)
    medical_card_id = Column(Integer, ForeignKey('medical_cards.id'))
    date = Column(Date)

    medical_card = relationship("MedicalCardModel", back_populates="diagnosis")


class Test(Base):
    __tablename__ = "tests"

    id = Column(Integer, primary_key=True, index=True) # noqa
    test_name = Column(String)
    result = Column(Text)
    file = Column(String)
    medical_card_id = Column(Integer, ForeignKey('medical_cards.id'))

    medical_card = relationship("MedicalCardModel", back_populates="tests")


class Procedure(Base):
    __tablename__ = "procedures"

    id = Column(Integer, primary_key=True, index=True) # noqa
    procedure_name = Column(String, nullable=False)
    description = Column(Text)
    date = Column(Date, nullable=False)
    doctor_id = Column(Integer, ForeignKey('users.id'))
    doctor_fullname = Column(String)
    medical_card_id = Column(Integer, ForeignKey('medical_cards.id'))

    medical_card = relationship("MedicalCardModel", back_populates="procedures")
