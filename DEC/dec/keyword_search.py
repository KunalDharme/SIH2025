import os
from PyPDF2 import PdfReader
import docx

def load_keywords(filepath="config/keywords.txt"):
    with open(filepath, "r", encoding="utf-8") as f:
        return [line.strip().lower() for line in f if line.strip()]

def search_in_txt(file_path, keywords):
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            text = f.read().lower()
            return [kw for kw in keywords if kw in text]
    except:
        return []

def search_in_pdf(file_path, keywords):
    matches = []
    try:
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        text = text.lower()
        matches = [kw for kw in keywords if kw in text]
    except:
        pass
    return matches

def search_in_docx(file_path, keywords):
    matches = []
    try:
        doc = docx.Document(file_path)
        text = "\n".join([p.text for p in doc.paragraphs]).lower()
        matches = [kw for kw in keywords if kw in text]
    except:
        pass
    return matches

def search_keywords(file_path, keywords):
    """
    Detect suspicious keywords inside TXT, PDF, DOCX files.
    Returns list of matches (empty if none).
    """
    ext = os.path.splitext(file_path)[1].lower()
    if ext == ".txt":
        return search_in_txt(file_path, keywords)
    elif ext == ".pdf":
        return search_in_pdf(file_path, keywords)
    elif ext in [".docx", ".doc"]:
        return search_in_docx(file_path, keywords)
    else:
        return []
