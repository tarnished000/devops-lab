import os
from datetime import datetime
from typing import List

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from fastapi.responses import Response

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://notes:notes@db:5432/notes",
)

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class Note(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    body = Column(String(2000), nullable=False, default="")
    created_at = Column(DateTime, default=datetime.utcnow)


Base.metadata.create_all(bind=engine)

app = FastAPI(title="notes-api")

REQUEST_COUNT = Counter(
    "notes_api_requests_total", "Total HTTP requests", ["method", "path", "status"]
)
REQUEST_LATENCY = Histogram(
    "notes_api_request_duration_seconds", "Request duration in seconds", ["method", "path"]
)


@app.middleware("http")
async def prometheus_middleware(request, call_next):
    import time

    start = time.perf_counter()
    response = await call_next(request)
    duration = time.perf_counter() - start
    REQUEST_COUNT.labels(request.method, request.url.path, response.status_code).inc()
    REQUEST_LATENCY.labels(request.method, request.url.path).observe(duration)
    return response


@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)


class NoteIn(BaseModel):
    title: str
    body: str = ""


class NoteOut(NoteIn):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/notes", response_model=List[NoteOut])
def list_notes():
    db = SessionLocal()
    try:
        return db.query(Note).order_by(Note.id.desc()).all()
    finally:
        db.close()


@app.post("/notes", response_model=NoteOut)
def create_note(note: NoteIn):
    db = SessionLocal()
    try:
        db_note = Note(title=note.title, body=note.body)
        db.add(db_note)
        db.commit()
        db.refresh(db_note)
        return db_note
    finally:
        db.close()


@app.get("/notes/{note_id}", response_model=NoteOut)
def get_note(note_id: int):
    db = SessionLocal()
    try:
        note = db.query(Note).filter(Note.id == note_id).first()
        if note is None:
            raise HTTPException(status_code=404, detail="Note not found")
        return note
    finally:
        db.close()


@app.delete("/notes/{note_id}")
def delete_note(note_id: int):
    db = SessionLocal()
    try:
        note = db.query(Note).filter(Note.id == note_id).first()
        if note is None:
            raise HTTPException(status_code=404, detail="Note not found")
        db.delete(note)
        db.commit()
        return {"status": "deleted", "id": note_id}
    finally:
        db.close()
