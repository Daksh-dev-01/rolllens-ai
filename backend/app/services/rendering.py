from pathlib import Path
import fitz

def inspect_pdf(path: Path):
    with fitz.open(path) as doc:
        if doc.is_encrypted: raise ValueError("Encrypted PDFs are not supported")
        if len(doc) < 1: raise ValueError("PDF has no pages")
        return [{"page_number": i+1, "width": float(p.rect.width), "height": float(p.rect.height), "text": p.get_text("text")} for i,p in enumerate(doc)]

def render_page(path: Path, page_number: int, scale: float = 1.5) -> bytes:
    with fitz.open(path) as doc:
        if page_number < 1 or page_number > len(doc): raise ValueError("Page number out of range")
        pix = doc[page_number-1].get_pixmap(matrix=fitz.Matrix(scale, scale), alpha=False)
        return pix.tobytes("png")
