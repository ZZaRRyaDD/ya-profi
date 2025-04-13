from pydantic import BaseModel, EmailStr, Field


class StudentCreate(BaseModel):
    name: str
    email: EmailStr | None = Field(default=None)
    group_id: int


class StudentInfo(BaseModel):
    id: int
    name: str
    group_id: int

    class Config:
        orm_mode = True

class StudentUpdate(StudentInfo):
    pass
