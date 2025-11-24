from typing import List

def load_txt(path: str) -> str:
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def load_pdf(path: str) -> str:
    try:
        from PyPDF2 import PdfReader
    except Exception:
        raise RuntimeError('PyPDF2 required to read PDFs. Install via pip.')
    reader = PdfReader(path)
    pages = []
    for p in reader.pages:
        text = p.extract_text()
        if text:
            pages.append(text)
    return "\n".join(pages)

def load_file(path: str) -> str:
    if path.lower().endswith('.pdf'):
        return load_pdf(path)
    else:
        return load_txt(path)

def chunk_text(text, chunk_size=1000, overlap=100):
    if not text:
        return []

    chunks = []
    length = len(text)

    # To avoid memory explosion
    max_allowed_size = 1000000  # 1 million characters

    if length > max_allowed_size:
        text = text[:max_allowed_size]

    start = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunks.append(text[start:end])
        start += chunk_size - overlap

    return chunks

