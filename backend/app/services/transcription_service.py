from datetime import datetime
from pathlib import Path
from app.core.config import settings


async def transcribe_audio(file_path: str):
    if not settings.openai_api_key:
        return {
            "text": "AI transcription not configured. Set OPENAI_API_KEY to enable transcription.",
            "status": "not_configured",
            "provider": "none",
            "created_at": datetime.utcnow(),
        }
    # Placeholder for OpenAI transcription integration.
    return {
        "text": f"Transcription placeholder for {Path(file_path).name}",
        "status": "completed",
        "provider": "openai",
        "created_at": datetime.utcnow(),
    }
