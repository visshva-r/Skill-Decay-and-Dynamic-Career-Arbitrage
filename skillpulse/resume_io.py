"""Resume upload parsing and GitHub username extraction."""
from __future__ import annotations

from urllib.parse import urlparse

from skillpulse.config import MAX_UPLOAD_SIZE_MB

try:
    import pdfplumber
except ImportError:
    pdfplumber = None

try:
    import docx as python_docx
except ImportError:
    python_docx = None


def extract_text_from_pdf(uploaded_file) -> str:
    if pdfplumber is None:
        return "[PDF extraction unavailable -- install pdfplumber]"
    text_parts = []
    with pdfplumber.open(uploaded_file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text_parts.append(page_text)
    return "\n".join(text_parts)


def extract_text_from_docx(uploaded_file) -> str:
    if python_docx is None:
        return "[DOCX extraction unavailable -- install python-docx]"
    doc = python_docx.Document(uploaded_file)
    return "\n".join(para.text for para in doc.paragraphs if para.text.strip())


def extract_text_from_upload(uploaded_file) -> str:
    if uploaded_file.size > MAX_UPLOAD_SIZE_MB * 1024 * 1024:
        return f"[File too large. Maximum allowed size is {MAX_UPLOAD_SIZE_MB} MB]"
    name = uploaded_file.name.lower()
    if name.endswith(".pdf"):
        return extract_text_from_pdf(uploaded_file)
    if name.endswith(".docx"):
        return extract_text_from_docx(uploaded_file)
    return uploaded_file.read().decode("utf-8", errors="replace")


def parse_github_username(raw_value: str) -> str:
    value = raw_value.strip()
    if not value:
        return ""
    if "github.com" not in value.lower():
        return value.lstrip("@").strip("/")
    parsed = urlparse(value)
    path_parts = [part for part in parsed.path.split("/") if part]
    return path_parts[0] if path_parts else ""
