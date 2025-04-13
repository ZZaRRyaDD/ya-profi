from fastapi import (
    APIRouter,
    Body,
    Depends,
    Path,
    Request,
    status,
    HTTPException,
)
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.connection import get_session
from app.db.repository import GroupRepository
from app.schemas.study import (
    GroupCreate,
    GroupCreateResponse,
    GroupUpdate,
    GroupInfo,
    GroupForList,
)
from app.utils import study as utils


api_router = APIRouter(
    prefix="/groups",
    tags=["Groups"],
)


@api_router.post(
    "",
    response_model=GroupCreateResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_group(
    _: Request,
    session: AsyncSession = Depends(get_session),
    group: GroupCreate = Body(...),
):
    created_group = await utils.create_group(session, group)
    return created_group


@api_router.get(
    "",
    response_model=list[GroupForList],
    status_code=status.HTTP_200_OK,
    response_model_exclude_none=True,
)
async def get_groups(
    _: Request,
    session: AsyncSession = Depends(get_session),
    query: str | None = None,
):
    groups = await utils.get_groups(session, query)
    if query != None:
        return groups

    for group in groups:
        group.subGroups = await utils.get_groups_by_parent_id(session, group.id)
    return groups

@api_router.get(
    "/{group_id}",
    response_model=GroupInfo,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_404_NOT_FOUND: {},
    },
)
async def get_group(
    _: Request,
    session: AsyncSession = Depends(get_session),
    group_id: int = Path(...),
):
    group = await utils.get_group(session, group_id)
    if not group:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return group


@api_router.put(
    "/{group_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_404_NOT_FOUND: {},
    },
)
async def update_group(
    _: Request,
    session: AsyncSession = Depends(get_session),
    group_id: int = Path(...),
    group: GroupUpdate = Body(...),
):
    repository = GroupRepository()
    group_db = await utils.get_group(session, group_id, repository=repository)
    if not group_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    await utils.update_group(session, group_db, group, repository=repository)


@api_router.delete(
    "/{group_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_404_NOT_FOUND: {},
    },
)
async def delete_group(
    _: Request,
    session: AsyncSession = Depends(get_session),
    group_id: int = Path(...),
):
    repository = GroupRepository()
    group_db = await utils.get_group(session, group_id, repository=repository)
    if not group_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    await utils.remove_group(session, group_id, repository=repository)
