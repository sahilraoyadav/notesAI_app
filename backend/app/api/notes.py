from pathlib import Path
from fastapi import APIRouter, Depends, File, UploadFile, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.models.note import Note
from app.schemas.note import NoteCreate, NoteOut, NoteUpdate
from app.services.ai import (
    summarize_text,
    describe_image,
    transcribe_voice,
    extract_reminder_from_text,
    embed_text,
    local_llm_chat,
)
from app.services.vector_store import vector_store
from app.services.json_store import json_note_store
from app.core.config import settings

router = APIRouter(prefix="/notes", tags=["notes"])


@router.post("", response_model=NoteOut)
async def create_note(payload: NoteCreate, db: AsyncSession = Depends(get_db)):
    note = Note(**payload.model_dump())
    if note.content:
        note.ai_summary = await summarize_text(note.content)
        note.reminder_at = await extract_reminder_from_text(note.content)
    db.add(note)
    await db.commit()
    await db.refresh(note)
    if note.content:
        vector_store.upsert(note.id, note.content, await embed_text(note.content))
    await json_note_store.export_notes(db)
    return note


@router.get("", response_model=list[NoteOut])
async def list_notes(db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(Note).order_by(Note.updated_at.desc()))
    return list(res.scalars().all())


@router.put("/{note_id}", response_model=NoteOut)
async def update_note(note_id: int, payload: NoteUpdate, db: AsyncSession = Depends(get_db)):
    note = await db.get(Note, note_id)
    if not note:
        raise HTTPException(404, "Note not found")
    for k, v in payload.model_dump(exclude_none=True).items():
        setattr(note, k, v)
    if note.content:
        note.ai_summary = await summarize_text(note.content)
    await db.commit()
    await db.refresh(note)
    await json_note_store.export_notes(db)
    return note


@router.delete("/{note_id}")
async def delete_note(note_id: int, db: AsyncSession = Depends(get_db)):
    note = await db.get(Note, note_id)
    if not note:
        raise HTTPException(404, "Note not found")
    await db.delete(note)
    await db.commit()
    await json_note_store.export_notes(db)
    return {"ok": True}


@router.post("/upload/{note_type}", response_model=NoteOut)
async def upload_note(note_type: str, title: str, file: UploadFile = File(...), db: AsyncSession = Depends(get_db)):
    if note_type not in {"image", "voice"}:
        raise HTTPException(400, "note_type must be image or voice")
    base = Path(settings.storage_path) / ("images" if note_type == "image" else "voice")
    base.mkdir(parents=True, exist_ok=True)
    path = base / file.filename
    path.write_bytes(await file.read())

    note = Note(title=title, note_type=note_type, media_path=str(path))
    if note_type == "image":
        note.ai_description = await describe_image(str(path))
        note.content = note.ai_description
    else:
        note.content = await transcribe_voice(str(path))
        note.ai_summary = await summarize_text(note.content)

    db.add(note)
    await db.commit()
    await db.refresh(note)
    vector_store.upsert(note.id, note.content or "", await embed_text(note.content or ""))
    await json_note_store.export_notes(db)
    return note


@router.get('/search', response_model=list[NoteOut])
async def search_notes(q: str, db: AsyncSession = Depends(get_db)):
    ids = vector_store.semantic_search(q)
    if not ids:
        return []
    res = await db.execute(select(Note).where(Note.id.in_(ids)))
    return list(res.scalars().all())


@router.get('/chat')
async def chat_with_notes(q: str, use_local_llm: bool = True, db: AsyncSession = Depends(get_db)):
    ids = vector_store.semantic_search(q)
    if not ids:
        return {"answer": "No related notes found."}
    res = await db.execute(select(Note).where(Note.id.in_(ids)))
    notes = list(res.scalars().all())
    context = "\n".join([f"[{n.id}] {n.title}: {n.content}" for n in notes])
    if use_local_llm:
        answer = await local_llm_chat(f"Use these notes as context:\n{context}\n\nQuestion: {q}")
        return {"answer": answer}
    return {"answer": f"Based on your notes:\n{context}"}
