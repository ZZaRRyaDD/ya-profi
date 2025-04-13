from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import INTEGER

from app.db import DeclarativeBase


class BaseTable(DeclarativeBase):
    __abstract__ = True

    id = Column(
        INTEGER,
        autoincrement=True,
        primary_key=True,
        unique=True,
        doc="Unique index of element",
    )

    def __repr__(self):
        columns = {column.name: getattr(self, column.name) for column in self.__table__.columns}
        return f'<{self.__tablename__}: {", ".join(map(lambda x: f"{x[0]}={x[1]}", columns.items()))}>'
