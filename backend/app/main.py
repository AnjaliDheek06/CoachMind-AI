from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database.init_db import create_tables
from app.upload_book.router import router as upload_book_router
from app.lesson.router import router as lesson_router
from app.scenario.router import router as scenario_router
from app.response.router import router as response_router
from app.evaluation.router import router as evaluation_router
from app.practice.router import router as practice_router

create_tables()

app = FastAPI(title="Communication Coach")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload_book_router)
app.include_router(lesson_router)
app.include_router(scenario_router)
app.include_router(response_router)
app.include_router(evaluation_router)
app.include_router(practice_router)


@app.get("/")
def root():
    return {
        "message": "Communication Coach Backend is running"
    }