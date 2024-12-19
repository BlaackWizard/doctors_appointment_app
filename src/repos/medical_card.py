from src.models.medical_card import (Diagnosis, MedicalCardModel, Procedure,
                                     Test, Visits)
from src.repos.sqlalchemy import SQLAlchemyRepo


class MedicalCardRepo(SQLAlchemyRepo):
    model = MedicalCardModel


class VisitsRepo(SQLAlchemyRepo):
    model = Visits


class DiagnosisRepo(SQLAlchemyRepo):
    model = Diagnosis


class TestsRepo(SQLAlchemyRepo):
    model = Test


class ProcedureRepo(SQLAlchemyRepo):
    model = Procedure
