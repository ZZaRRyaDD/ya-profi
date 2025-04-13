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
from app.db.repository import StudentRepository
from app.schemas.study import (
    StudentCreate,
    StudentInfo,
    StudentUpdate,
)
from app.utils import study as utils


api_router = APIRouter(
    prefix="/students",
    tags=["Students"],
)


@api_router.post(
    "",
    response_model=StudentInfo,
    responses={
        status.HTTP_201_CREATED: {},
        status.HTTP_404_NOT_FOUND: {},
    },
)
async def create_student(
    _: Request,
    session: AsyncSession = Depends(get_session),
    student: StudentCreate = Body(...),
):
    group = await utils.get_group(session, student.group_id)
    if not group:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    created_student = await utils.create_student(session, student)
    return created_student


@api_router.get(
    "",
    response_model=list[StudentInfo],
    status_code=status.HTTP_200_OK,
)
async def get_student(
    _: Request,
    session: AsyncSession = Depends(get_session),
    query: str | None = None,
):
    students = await utils.get_students(session, query)
    return students

@api_router.get(
    "/{student_id}",
    response_model=StudentInfo,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_404_NOT_FOUND: {},
    },
)
async def get_student(
    _: Request,
    session: AsyncSession = Depends(get_session),
    student_id: int = Path(...),
):
    student = await utils.get_student(session, student_id)
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return student


@api_router.put(
    "/{student_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_404_NOT_FOUND: {},
    },
)
async def update_student(
    _: Request,
    session: AsyncSession = Depends(get_session),
    student_id: int = Path(...),
    student: StudentUpdate = Body(...),
):
    group = await utils.get_group(session, student.group_id)
    if not group:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    repository = StudentRepository()
    student_db = await utils.get_student(session, student_id, repository=repository)
    if not student_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    await utils.update_student(session, student_db, student, repository=repository)


@api_router.delete(
    "/{student_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_404_NOT_FOUND: {},
    },
)
async def delete_student(
    _: Request,
    session: AsyncSession = Depends(get_session),
    student_id: int = Path(...),
):
    repository = StudentRepository()
    student_db = await utils.get_student(session, student_id, repository=repository)
    if not student_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    await utils.remove_student(session, student_id, repository=repository)
