from .base import BaseTable

from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.dialects.postgresql import TEXT, INTEGER


class Group(BaseTable):
    __tablename__ = "group"

    name = Column(
        TEXT,
        nullable=False,
        doc="Название группы",
    )
    parent_id = Column(
        INTEGER,
        ForeignKey("group.id"),
        nullable=True,
    )

    students = relationship("Student", back_populates="group")
    