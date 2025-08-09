from sqlalchemy import Column, Integer, String, Boolean
from app.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    completed = Column(Boolean, default=False)

    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="tasks")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    task = relationship("Task", back_populates="owner")
