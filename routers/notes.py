from anyio import sleep
from fastapi import APIRouter
from time import sleep
from fastapi import HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
from app.models import NoteCreate
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel
from dotenv import load_dotenv
import os

load_dotenv()

router = APIRouter()

notes = []

engine = create_engine(os.getenv("DATABASE_URL"))

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class NotesCreate(BaseModel):
    __tablename__ = "notes"
    id: int = Column(Integer, primary_key=True, index=True)
    title: str = Column(String, index=True)
    content: str = Column(String, index=True)
    created_at: str = Column(String, index=True)


Base.metadata.create_all(bind=engine)


class NoteCreate(BaseModel):
    id: int
    title: str
    content: str
    created_at: str


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


get_db()


def custom_success_message(message: str):
    sleep(4)
    return JSONResponse(content={"message": message})


@router.post("/notes", response_model=NoteCreate)
# get the ids increment by 1 while creating a note
async def create_note(note: NoteCreate, background_tasks: BackgroundTasks):

    background_tasks.add_task(
        custom_success_message, f"note id:{note.id} created successfully"
    )
    if len(notes) == 0:
        note.id = len(notes) + 1
    else:
        note.id = notes[-1].id + 1

    notes.append(note)
    return note


@router.get("/notes")
async def read_notes():
    return notes


@router.get("/notes/{id}", response_model=NoteCreate)
async def read_note(note_id: int, background_tasks: BackgroundTasks):
    for note in notes:
        if note.id == note_id:
            background_tasks.add_task(
                custom_success_message, f"note id:{note_id} retrieved successfully"
            )
            return note
    raise HTTPException(status_code=404, detail=f"Note with id:{note_id} is not found")


@router.put("/notes/{id}", response_model=NoteCreate)
async def update_note(
    note_id: int, updated_note: NoteCreate, background_tasks: BackgroundTasks
):
    for note in notes:
        if note.id == note_id:
            background_tasks.add_task(
                custom_success_message, f"note id:{note_id} updated successfully"
            )
            note.title = updated_note.title
            note.content = updated_note.content
        return note
    raise HTTPException(status_code=404, detail=f"Note with id:{note_id} not found")


@router.delete("/notes/{id}", response_model=NoteCreate)
async def delete_note(note_id: int, background_tasks: BackgroundTasks):
    for note in notes:
        if note.id == note_id:
            background_tasks.add_task(
                custom_success_message, f"note id:{note_id} deleted successfully"
            )
            notes.remove(note)
        return note
    raise HTTPException(status_code=404, detail=f"Note with id:{note_id}not found")
