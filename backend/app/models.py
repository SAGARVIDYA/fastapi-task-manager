from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base


# User Table
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    username = Column(String(100), unique=True, nullable=False)

    password = Column(String(255), nullable=False)

    # relationship with tasks
    tasks = relationship("Task", back_populates="owner")


# Task Table
class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String(255), nullable=False)

    description = Column(String(500), nullable=True)

    completed = Column(Boolean, default=False)

    owner_id = Column(Integer, ForeignKey("users.id"))

    # relationship with user
    owner = relationship("User", back_populates="tasks")