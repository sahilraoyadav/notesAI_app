# NotesAI App (FastAPI + React)

## Features
- CRUD notes with local SQLite.
- Voice note recording in the browser (MediaRecorder), playback, rename, delete, and attach to notes.
- Image uploads with preview thumbnails.
- Optional AI transcription and OCR with graceful local fallback when `OPENAI_API_KEY` is not configured.

## Complete Anaconda setup (recommended)
1. Install Anaconda or Miniconda.
2. `conda env create -f environment.yml`
3. `conda activate notesai`

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

## Voice Notes
- Record directly in Note Editor (`Idle`, `Recording`, `Paused`, `Processing`, `Saved`, `Error` states).
- Save audio attachments via `POST /api/notes/{note_id}/voice-notes`.
- Supported audio upload types: `webm`, `wav`, `mp3`, `m4a`.
- Stored locally under `backend/uploads/audio/`.

## Image-to-Text OCR
- Upload image attachments (`png`, `jpg`, `jpeg`, `webp`) with thumbnail previews.
- Extract text from one image: `POST /api/attachments/{attachment_id}/extract-text`.
- Extract text from all images on note: `POST /api/notes/{note_id}/extract-text-from-images`.
- Stored locally under `backend/uploads/images/`.

## Transcription
- Single audio: `POST /api/attachments/{attachment_id}/transcribe`.
- All audio for note: `POST /api/notes/{note_id}/transcribe-voice-notes`.
- If `OPENAI_API_KEY` is missing, responses are friendly fallback messages (app still fully usable).

## Upload storage and static serving
- `backend/uploads/audio/` exposed at `/uploads/audio/`
- `backend/uploads/images/` exposed at `/uploads/images/`
- `backend/uploads/files/` exposed at `/uploads/files/`

## Optional env
- `OPENAI_API_KEY` (optional). Never hardcode this key.

## Local-only limitations
- Without OpenAI configured, transcription/OCR return `not_configured` mock responses.
- Voice recording, playback, image upload, and attachment management continue working locally.
