# NotesAI App (FastAPI + React)

## Features
- CRUD for text/image/voice notes (SQLite metadata + local media storage).
- AI hooks for image description + OCR, voice transcription, note summaries.
- NLP reminder extraction from natural language note content.
- Semantic search and simple RAG-style "chat with notes" endpoint.
- Kanban UI (Todo/Doing/Done) with dark-mode friendly Tailwind styling.

## Backend
```bash
cd backend
uvicorn app.main:app --reload --port 8000
```

## Frontend
```bash
cd frontend
npm install
npm run dev
```

## API highlights
- `POST /notes` text note CRUD create
- `POST /notes/upload/image` image note upload + AI description
- `POST /notes/upload/voice` voice note upload + transcription
- `GET /notes/search?q=...` semantic search
- `GET /chat?q=...` ask questions across notes context

## Notes
- `app/services/ai.py` contains async placeholders to swap with OpenAI GPT-4o/Whisper calls.
- `app/services/vector_store.py` uses an in-memory adapter; replace with ChromaDB/FAISS persistence for production.
