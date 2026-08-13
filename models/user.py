from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(min_length=3, max_length=50, unique=True, index=True)
    email: str = Field(unique=True, index=True)
    hashed_password: str
    full_name: str = Field(min_length=2, max_length=100)
    role: str = Field(default="patient")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    is_active: bool = Field(default=True)


class UserCreate(SQLModel):
    username: str = Field(min_length=3, max_length=50)
    email: str
    password: str = Field(min_length=8)
    full_name: str = Field(min_length=2, max_length=100)
    role: str = Field(default="patient")


class UserLogin(SQLModel):
    username: str
    password: str


class UserResponse(SQLModel):
    id: int
    username: str
    email: str
    full_name: str
    role: str
    created_at: datetime
    is_active: bool