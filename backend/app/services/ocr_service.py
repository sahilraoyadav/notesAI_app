from datetime import datetime
from pathlib import Path
from app.core.config import settings


async def extract_text_from_image(file_path: str):
    if not settings.openai_api_key:
        return {
            "text": "AI extraction not configured. Set OPENAI_API_KEY to enable OCR.",
            "status": "not_configured",
            "provider": "none",
            "created_at": datetime.utcnow(),
        }
    return {
        "text": f"OCR placeholder for {Path(file_path).name}",
        "status": "completed",
        "provider": "openai",
        "created_at": datetime.utcnow(),
    }
