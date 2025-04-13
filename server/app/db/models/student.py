from .base import BaseTable

from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import TEXT, INTEGER


class Student(BaseTable):
    __tablename__ = "student"

    name = Column(
        TEXT,
        nullable=False,
        doc="Имя участника",
    )
    email = Column(
        TEXT,
        nullable=False,
        doc="Email участника",
    )
    group_id = Column(
        INTEGER,
        ForeignKey("group.id"),
        nullable=False,
    )
    group = relationship(
        "Group",
        back_populates="students",
    )