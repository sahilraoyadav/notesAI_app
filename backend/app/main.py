from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.notes import router as notes_router
from app.db.base import Base
from app.db.session import engine

app = FastAPI(title="NotesAI")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
app.include_router(notes_router)


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.get('/health')
async def health():
    return {"status": "ok"}
