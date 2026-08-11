# app/evaluation/model.py
from sqlalchemy import Column, ForeignKey, Integer, Text
from sqlalchemy.orm import relationship

from app.database.database import Base


class Evaluation(Base):
    __tablename__ = "evaluations"

    id = Column(Integer, primary_key=True, index=True)

    response_id = Column(
        Integer,
        ForeignKey("responses.id"),
        nullable=False
    )

    lesson_objective_status = Column(Text, nullable=False)
    communication_analysis = Column(Text, nullable=False)
    language_analysis = Column(Text, nullable=False)
    communication_improvements = Column(Text, nullable=False)
    grammar_corrections = Column(Text, nullable=False)
    micro_improvements = Column(Text, nullable=False)

    response = relationship(
        "Response",
        back_populates="evaluation"
    )

    coaching = relationship(
        "Coaching",
        back_populates="evaluation",
        cascade="all, delete",
        uselist=False
    )