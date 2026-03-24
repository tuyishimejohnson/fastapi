from fastapi import APIRouter
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from app.schemas import NoteCreate


router = APIRouter()

notes = []
@router.post("/notes", response_model=NoteCreate)
# get the ids increment by 1 while creating a note


def create_note(note: NoteCreate):
    if not notes:
        note.id = 1
    else:
        note.id = len(list(n.id for n in notes)) + 1

    notes.append(note)
    return note


@router.get("/notes")
def read_notes():
    return notes


@router.get("/notes/{id}", response_model=NoteCreate)
def read_note(note_id: int):
    for note in notes:
        if note.id == note_id:
            return note
        raise HTTPException(
            status_code=404, detail=f"Note with id:{note_id} is not found"
        )
    return None


@router.put("/notes/{id}", response_model=NoteCreate)
def update_note(note_id: int, updated_note: NoteCreate):
    for note in notes:
        if note.id != note_id:
            raise HTTPException(
                status_code=404, detail=f"Note with id:{note_id} not found"
            )
        note.id = note_id
        note.title = updated_note.title
        note.content = updated_note.content
        return note
    return None


@router.delete("/notes/{id}", response_model=NoteCreate)
def delete_note(note_id: int):
    for note in notes:
        if note.id == note_id:
            notes.remove(note)
            return note
        raise HTTPException(
            status_code=404, detail=f"Note with id:{note_id}not found"
        )
    return None
