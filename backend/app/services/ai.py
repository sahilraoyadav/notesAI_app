import asyncio
from datetime import datetime
from dateutil.parser import parse as dt_parse


async def summarize_text(text: str) -> str:
    await asyncio.sleep(0)
    lines = [line.strip() for line in text.split(".") if line.strip()][:3]
    return "\n".join([f"- {line}" for line in lines]) if lines else "- No summary available"


async def describe_image(_path: str) -> str:
    await asyncio.sleep(0)
    return "Image uploaded. Vision/OCR pipeline placeholder description."


async def transcribe_voice(_path: str) -> str:
    await asyncio.sleep(0)
    return "Voice transcription placeholder. Integrate Whisper/OpenAI audio API."


async def extract_reminder_from_text(text: str) -> datetime | None:
    await asyncio.sleep(0)
    if "remind me" not in text.lower():
        return None
    try:
        return dt_parse(text, fuzzy=True)
    except Exception:
        return None


async def embed_text(_text: str) -> list[float]:
    await asyncio.sleep(0)
    return [0.1, 0.2, 0.3]
