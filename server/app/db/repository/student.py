from .base import BaseRepository
from app.db.models import Student, Group
from app.schemas.study import StudentCreate, StudentUpdate

from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession


class StudentRepository(BaseRepository[Student, StudentCreate, StudentUpdate]):
    def __init__(self):
        super().__init__(Student)

    async def get_multi(self, session: AsyncSession, search_query: str | None) -> list[Student]:
        query = select(self.model)
        if search_query not in ("" , None):
            query = query.join(Group).filter(
                or_(
                    self.model.name.like(f"%{search_query}%"),
                    Group.name.like(f"%{search_query}%"),
                ),
            )
        result = await session.execute(query)
        return result.scalars().all()
