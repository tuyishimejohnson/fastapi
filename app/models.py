from pydantic import BaseModel
from datetime import datetime
from sqlmodel import SQLModel, Field
from sqlalchemy import Column, Integer, String


class NoteCreate(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    title: str
    content: str
    created_at: datetime = Field(default_factory=datetime.now)


class NotesCreate(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    title: str
    content: str
    created_at: datetime = Field(default_factory=datetime.now)
