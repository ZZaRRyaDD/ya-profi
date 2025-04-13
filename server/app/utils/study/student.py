from app.db.models import Student
from app.db.repository import StudentRepository


async def create_student(session, student_body, repository = StudentRepository()):
    return await repository.create(session, obj_in=student_body)


async def get_student(session, student_id: int, repository = StudentRepository()):
    return await repository.get_by_id(session, obj_id=student_id)

async def get_students(session, query: str, repository = StudentRepository()):
    return await repository.get_multi(session, query)


async def update_student(session, student_db: Student, student_body, repository = StudentRepository()):
    return await repository.update(session, db_obj=student_db, obj_in=student_body)


async def remove_student(session, student_id: int, repository = StudentRepository()):
    return await repository.remove(session, obj_id=student_id)