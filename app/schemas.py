# app/schemas.py
from pydantic import BaseModel
from typing import Optional, List

# ======================
# 🔹 Schemas de Tarefas
# ======================


class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None


class TaskRead(TaskCreate):
    id: int
    completed: bool

    class Config:
        orm_mode = True


# ======================
# 🔹 Schemas de Usuários
# ======================


class UserCreate(BaseModel):
    username: str
    password: str


class UserRead(BaseModel):
    id: int
    username: str

    class Config:
        orm_mode = True


# ======================
# 🔹 Schemas de Autenticação (JWT)
# ======================


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    username: Optional[str] = None
