from pathlib import Path
import hashlib, re, uuid
from fastapi import UploadFile, HTTPException
from app.config import settings

async def save_upload(file: UploadFile) -> tuple[Path, str, int]:
    name = Path(file.filename or "").name
    if not name.lower().endswith(".pdf"): raise HTTPException(415, "Only PDF files are accepted")
    if not re.fullmatch(r"[\w .()\-]{1,180}\.pdf", name, flags=re.IGNORECASE): raise HTTPException(400, "Unsafe filename")
    data = await file.read(settings.max_upload_mb * 1024 * 1024 + 1)
    if len(data) > settings.max_upload_mb * 1024 * 1024: raise HTTPException(413, "Upload exceeds size limit")
    if not data.startswith(b"%PDF-"): raise HTTPException(400, "File does not appear to be a PDF")
    root = settings.storage_dir.resolve(); root.mkdir(parents=True, exist_ok=True)
    path = root / f"{uuid.uuid4().hex}.pdf"
    path.write_bytes(data)
    return path, hashlib.sha256(data).hexdigest(), len(data)
