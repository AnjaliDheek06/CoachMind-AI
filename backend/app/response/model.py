# app/response/model.py
from sqlalchemy import Column, ForeignKey, Integer, Text
from sqlalchemy.orm import relationship

from app.database.database import Base


class Response(Base):
    __tablename__ = "responses"

    id = Column(Integer, primary_key=True, index=True)

    scenario_id = Column(
        Integer,
        ForeignKey("scenarios.id"),
        nullable=False
    )

    content = Column(Text, nullable=False)

    scenario = relationship(
        "Scenario",
        back_populates="responses"
    )

    evaluation = relationship(
        "Evaluation",
        back_populates="response",
        cascade="all, delete",
        uselist=False
    )