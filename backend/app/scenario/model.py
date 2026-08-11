# app/scenario/model.py
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database.database import Base


class Scenario(Base):
    __tablename__ = "scenarios"

    id = Column(Integer, primary_key=True, index=True)

    lesson_id = Column(
        Integer,
        ForeignKey("lessons.id"),
        nullable=False
    )

    title = Column(String, nullable=False)
    context = Column(String, nullable=False)
    objective = Column(String, nullable=False)

    is_completed = Column(Boolean, default=False, nullable=False)

    lesson = relationship(
        "Lesson",
        back_populates="scenarios"
    )

    responses = relationship(
        "Response",
        back_populates="scenario",
        cascade="all, delete"
    )