from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from routers import notes

app = FastAPI()
app.include_router(notes.router)


