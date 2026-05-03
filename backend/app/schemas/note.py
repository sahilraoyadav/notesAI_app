from datetime import datetime
from pydantic import BaseModel, Field


class NoteBase(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    content: str | None = None
    status: str = "todo"


class NoteCreate(NoteBase):
    note_type: str = "text"


class NoteUpdate(BaseModel):
    title: str | None = None
    content: str | None = None
    status: str | None = None
    reminder_at: datetime | None = None


class NoteOut(NoteBase):
    id: int
    note_type: str
    media_path: str | None
    ai_summary: str | None
    ai_description: str | None
    reminder_at: datetime | None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
