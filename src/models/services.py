from sqlalchemy import Column, Float, Integer, String
from sqlalchemy.orm import relationship

from src.db.connect import Base


class Services(Base):
    __tablename__ = "services"

    id = Column(Integer, primary_key=True) # noqa

    title = Column(String, nullable=False)
    cost = Column(Float, nullable=False)
    requisites = Column(String, nullable=False)

    payment = relationship(
        "Payment",
        back_populates="service",
        foreign_keys="[Payment.service_id]",
    )

    def __str__(self):
        return f'Услуга {self.title}'
