from datetime import datetime
from typing import List
import uuid
from pydantic import BaseModel, EmailStr, constr, Field
from enum import Enum

class TaskStatusEnum(str, Enum):
    Pending = "Pending"
    Doing = "Doing"
    Blocked = "Blocked"
    Done = "Done"

class UserBaseSchema(BaseModel):
    name: str
    email: EmailStr

    class Config:
        from_attributes = True


class CreateUserSchema(UserBaseSchema):
    password: str = Field(max_length=8)
    passwordConfirm: str
    role: str = 'user'
    verified: bool = False


class LoginUserSchema(BaseModel):
    email: EmailStr
    password: str = Field(max_length=8)


class UserResponse(UserBaseSchema):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime


class FilteredUserResponse(UserBaseSchema):
    id: uuid.UUID

class TaskBaseSchema(BaseModel):
    title: str
    content: str
    category: str
    user_id: uuid.UUID | None = None
    status: TaskStatusEnum

    class Config:
        from_attributes = True

class CreateTaskSchema(TaskBaseSchema):
    pass

class TaskResponse(TaskBaseSchema):
    id: uuid.UUID
    user: FilteredUserResponse
    created_at: datetime
    updated_at: datetime

class UpdateTaskSchema(BaseModel):
    title: str
    content: str
    category: str
    user_id: uuid.UUID | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    class Config:
        orm_mode = True


class ListTaskResponse(BaseModel):
    status: str
    results: int
    posts: List[TaskResponse]