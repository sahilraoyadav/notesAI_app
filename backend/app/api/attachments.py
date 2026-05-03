from datetime import datetime
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.db.session import get_db
from app.models.attachment import Attachment
from app.models.note import Note
from app.services.file_storage_service import save_upload
from app.services.ocr_service import extract_text_from_image
from app.services.transcription_service import transcribe_audio

router = APIRouter(prefix="/api", tags=["attachments"])


@router.post("/notes/{note_id}/attachments")
async def upload_attachment(note_id: int, attachment_type: str, file: UploadFile = File(...), db: AsyncSession = Depends(get_db)):
    note = await db.get(Note, note_id)
    if not note:
        raise HTTPException(404, "Note not found")
    meta = await save_upload(file, "backend/uploads", attachment_type)
    att = Attachment(note_id=note_id, attachment_type=attachment_type, file_type=attachment_type, duration_seconds=None, **meta)
    db.add(att)
    await db.commit()
    await db.refresh(att)
    return att


@router.post("/notes/{note_id}/voice-notes")
async def upload_voice_note(note_id: int, file: UploadFile = File(...), db: AsyncSession = Depends(get_db)):
    return await upload_attachment(note_id, "audio", file, db)


@router.get("/notes/{note_id}/attachments")
async def list_attachments(note_id: int, db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(Attachment).where(Attachment.note_id == note_id).order_by(Attachment.created_at.desc()))
    return list(res.scalars().all())


@router.delete("/attachments/{attachment_id}")
async def delete_attachment(attachment_id: int, db: AsyncSession = Depends(get_db)):
    att = await db.get(Attachment, attachment_id)
    if not att:
        raise HTTPException(404, "Attachment not found")
    await db.delete(att)
    await db.commit()
    return {"ok": True}


@router.post("/attachments/{attachment_id}/transcribe")
async def transcribe_attachment(attachment_id: int, db: AsyncSession = Depends(get_db)):
    att = await db.get(Attachment, attachment_id)
    if not att or att.attachment_type != "audio":
        raise HTTPException(404, "Audio attachment not found")
    data = await transcribe_audio(att.file_path)
    att.transcript_text = data["text"]
    att.transcript_status = data["status"]
    att.transcript_created_at = data["created_at"]
    await db.commit()
    return {"attachment_id": att.id, **data}


@router.post("/notes/{note_id}/transcribe-voice-notes")
async def transcribe_note_voice_notes(note_id: int, db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(Attachment).where(Attachment.note_id == note_id, Attachment.attachment_type == "audio"))
    items = list(res.scalars().all())
    out = []
    for att in items:
        data = await transcribe_audio(att.file_path)
        att.transcript_text = data["text"]
        att.transcript_status = data["status"]
        att.transcript_created_at = data["created_at"]
        out.append({"attachment_id": att.id, **data})
    await db.commit()
    return out


@router.post("/attachments/{attachment_id}/extract-text")
async def extract_attachment_text(attachment_id: int, db: AsyncSession = Depends(get_db)):
    att = await db.get(Attachment, attachment_id)
    if not att or att.attachment_type != "image":
        raise HTTPException(404, "Image attachment not found")
    data = await extract_text_from_image(att.file_path)
    att.extracted_text = data["text"]
    att.extraction_status = data["status"]
    att.extraction_created_at = data["created_at"]
    await db.commit()
    return {"attachment_id": att.id, **data}


@router.post("/notes/{note_id}/extract-text-from-images")
async def extract_note_image_text(note_id: int, db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(Attachment).where(Attachment.note_id == note_id, Attachment.attachment_type == "image"))
    items = list(res.scalars().all())
    out = []
    for att in items:
        data = await extract_text_from_image(att.file_path)
        att.extracted_text = data["text"]
        att.extraction_status = data["status"]
        att.extraction_created_at = data["created_at"]
        out.append({"attachment_id": att.id, **data})
    await db.commit()
    return out
