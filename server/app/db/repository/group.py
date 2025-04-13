from .base import BaseRepository
from app.db.models import Group
from app.schemas.study import GroupCreate

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class GroupRepository(BaseRepository[Group, GroupCreate, GroupCreate]):
    def __init__(self):
        super().__init__(Group)

    async def get_multi(self, session: AsyncSession, search_query: str | None) -> list[Group]:
        query = select(self.model)
        if search_query not in ("" , None):
            query = query.filter(self.model.name.like(f"%{search_query}%"))
        result = await session.execute(query)
        return result.scalars().all()

    async def get_multi_by_parent_id(self, session: AsyncSession, parent_id: int) -> list[Group]:
        query = select(self.model).filter(self.model.parent_id == parent_id)
        result = await session.execute(query)
        return result.scalars().all()
