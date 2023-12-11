from datetime import datetime
from typing import List
import uuid
from pydantic import BaseModel, EmailStr, constr, Field


class UserBaseSchema(BaseModel):
    name: str
    email: EmailStr
    photo: str

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

class PostBaseSchema(BaseModel):
    title: str
    content: str
    category: str
    image: str
    user_id: uuid.UUID | None = None

    class Config:
        from_attributes = True

class CreatePostSchema(PostBaseSchema):
    pass

class PostResponse(PostBaseSchema):
    id: uuid.UUID
    user: FilteredUserResponse
    created_at: datetime
    updated_at: datetime

class UpdatePostSchema(BaseModel):
    title: str
    content: str
    category: str
    image: str
    user_id: uuid.UUID | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    class Config:
        orm_mode = True


class ListPostResponse(BaseModel):
    status: str
    results: int
    posts: List[PostResponse]