from __future__ import annotations

import json
from pathlib import Path
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.note import Note


class JsonNoteStore:
    def __init__(self, folder: str = "backend/storage/json") -> None:
        self.path = Path(folder)
        self.path.mkdir(parents=True, exist_ok=True)
        self.file = self.path / "notes.json"

    async def export_notes(self, db: AsyncSession) -> None:
        res = await db.execute(select(Note).order_by(Note.id.asc()))
        notes = res.scalars().all()
        payload = [
            {
                "id": n.id,
                "title": n.title,
                "content": n.content,
                "note_type": n.note_type,
                "status": n.status,
                "media_path": n.media_path,
                "ai_summary": n.ai_summary,
                "ai_description": n.ai_description,
                "reminder_at": n.reminder_at.isoformat() if n.reminder_at else None,
                "created_at": n.created_at.isoformat(),
                "updated_at": n.updated_at.isoformat(),
            }
            for n in notes
        ]
        self.file.write_text(json.dumps(payload, indent=2), encoding="utf-8")


json_note_store = JsonNoteStore()
