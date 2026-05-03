from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api.notes import router as notes_router
from app.api.attachments import router as attachments_router
from app.db.base import Base
from app.db.session import engine
from app.models import note as _note  # noqa
from app.models import attachment as _attachment  # noqa

app = FastAPI(title="NotesAI")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
app.include_router(notes_router)
app.include_router(attachments_router)

Path("backend/uploads/audio").mkdir(parents=True, exist_ok=True)
Path("backend/uploads/images").mkdir(parents=True, exist_ok=True)
Path("backend/uploads/files").mkdir(parents=True, exist_ok=True)
app.mount("/uploads/audio", StaticFiles(directory="backend/uploads/audio"), name="uploads_audio")
app.mount("/uploads/images", StaticFiles(directory="backend/uploads/images"), name="uploads_images")
app.mount("/uploads/files", StaticFiles(directory="backend/uploads/files"), name="uploads_files")


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.get('/health')
async def health():
    return {"status": "ok"}
