import mimetypes
import secrets
from pathlib import Path
from fastapi import HTTPException, UploadFile

MAX_UPLOAD_BYTES = 20 * 1024 * 1024
ALLOWED = {
    "audio": {"ext": {".webm", ".wav", ".mp3", ".m4a"}, "mime_prefix": "audio/", "dir": "audio"},
    "image": {"ext": {".png", ".jpg", ".jpeg", ".webp"}, "mime_prefix": "image/", "dir": "images"},
    "file": {"ext": {".txt", ".md", ".pdf"}, "mime_prefix": None, "dir": "files"},
}


def _safe_name(ext: str) -> str:
    return f"{secrets.token_hex(12)}{ext}"


async def save_upload(upload: UploadFile, root: str, attachment_type: str):
    if attachment_type not in ALLOWED:
        raise HTTPException(400, "Unsupported attachment type")
    ext = Path(upload.filename or "").suffix.lower()
    cfg = ALLOWED[attachment_type]
    if ext not in cfg["ext"]:
        raise HTTPException(400, f"Unsupported extension: {ext}")
    mime = upload.content_type or mimetypes.guess_type(upload.filename or "")[0] or "application/octet-stream"
    if cfg["mime_prefix"] and not mime.startswith(cfg["mime_prefix"]):
        raise HTTPException(400, "Invalid MIME type")

    data = await upload.read()
    if len(data) > MAX_UPLOAD_BYTES:
        raise HTTPException(413, "File too large")

    base = Path(root) / cfg["dir"]
    base.mkdir(parents=True, exist_ok=True)
    filename = _safe_name(ext)
    path = base / filename
    path.write_bytes(data)
    return {
        "filename": filename,
        "original_filename": upload.filename or filename,
        "mime_type": mime,
        "file_path": str(path),
        "size_bytes": len(data),
    }
