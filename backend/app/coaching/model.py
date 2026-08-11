# app/coaching/model.py
from sqlalchemy import Column, ForeignKey, Integer, Text
from sqlalchemy.orm import relationship

from app.database.database import Base


class Coaching(Base):
    __tablename__ = "coachings"

    id = Column(Integer, primary_key=True, index=True)

    evaluation_id = Column(
        Integer,
        ForeignKey("evaluations.id"),
        nullable=False,
        unique=True
    )

    key_improvements = Column(Text, nullable=False)
    why_it_matters = Column(Text, nullable=False)
    next_scenario_focus = Column(Text, nullable=False)

    evaluation = relationship(
        "Evaluation",
        back_populates="coaching"
    )