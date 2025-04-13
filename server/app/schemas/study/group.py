from pydantic import BaseModel


class GroupCreate(BaseModel):
    name: str
    parent_id: int | None


class GroupCreateResponse(BaseModel):
    id: int
    name: str
    parent_id: int | None
    
    class Config:
        orm_mode = True


class GroupUpdate(GroupCreate):
    id: int


class GroupInfo(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class GroupForList(BaseModel):
    id: int
    name: str
    subGroups: list[GroupInfo] | None

    class Config:
        orm_mode = True
