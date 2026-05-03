from datetime import datetime
from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Attachment(Base):
    __tablename__ = "attachments"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    note_id: Mapped[int] = mapped_column(ForeignKey("notes.id", ondelete="CASCADE"), index=True)
    filename: Mapped[str] = mapped_column(String(255))
    original_filename: Mapped[str] = mapped_column(String(255))
    attachment_type: Mapped[str] = mapped_column(String(32), index=True)
    file_type: Mapped[str] = mapped_column(String(32), default="file")
    mime_type: Mapped[str] = mapped_column(String(128))
    file_path: Mapped[str] = mapped_column(String(512))
    size_bytes: Mapped[int] = mapped_column(Integer)
    duration_seconds: Mapped[float | None] = mapped_column(Float, nullable=True)

    transcript_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    transcript_status: Mapped[str | None] = mapped_column(String(32), nullable=True)
    transcript_created_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    extracted_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    extraction_status: Mapped[str | None] = mapped_column(String(32), nullable=True)
    extraction_created_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    note = relationship("Note", back_populates="attachments")
