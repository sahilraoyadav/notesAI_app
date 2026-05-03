# NotesAI App (FastAPI + React)

## Features
- CRUD for text/image/voice notes (SQLite metadata + local media storage).
- AI hooks for image description + OCR, voice transcription, note summaries.
- NLP reminder extraction from natural language note content.
- Semantic search and simple RAG-style "chat with notes" endpoint.
- Kanban UI (Todo/Doing/Done) with dark-mode friendly Tailwind styling.

## Complete Anaconda setup (recommended)
1. Install Anaconda or Miniconda:
   - Anaconda: https://www.anaconda.com/download
   - Miniconda: https://docs.conda.io/en/latest/miniconda.html
2. Open a new terminal and go to the project root:
   ```bash
   cd /path/to/notesAI_app
   ```
3. Create the environment from `environment.yml`:
   ```bash
   conda env create -f environment.yml
   ```
4. Activate the environment:
   ```bash
   conda activate notesai
   ```
5. Verify key tools were installed:
   ```bash
   python --version
   node --version
   pip --version
   ```
6. (If dependencies change later) update the same environment:
   ```bash
   conda env update -f environment.yml --prune
   ```
7. (Optional) remove and recreate environment cleanly:
   ```bash
   conda deactivate
   conda env remove -n notesai
   conda env create -f environment.yml
   conda activate notesai
   ```

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
