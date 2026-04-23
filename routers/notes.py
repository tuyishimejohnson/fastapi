from anyio import sleep
from fastapi import APIRouter
from time import sleep
from fastapi import HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
from app.schemas import NoteCreate


router = APIRouter()

notes = []


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
