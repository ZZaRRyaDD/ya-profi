from app.db.models import Group
from app.db.repository import GroupRepository


async def create_group(session, group_body, repository = GroupRepository()):
    return await repository.create(session, obj_in=group_body)


async def get_group(session, group_id: int, repository = GroupRepository()):
    return await repository.get_by_id(session, obj_id=group_id)


async def get_groups(session, query: str | None, repository = GroupRepository()):
    return await repository.get_multi(session, query)


async def get_groups_by_parent_id(session, parent_id: int, repository = GroupRepository()):
    return await repository.get_multi_by_parent_id(session, parent_id)

async def update_group(session, group_db: Group, group_body, repository = GroupRepository()):
    return await repository.update(session, db_obj=group_db, obj_in=group_body)


async def remove_group(session, group_id: int, repository = GroupRepository()):
    return await repository.remove(session, obj_id=group_id)
