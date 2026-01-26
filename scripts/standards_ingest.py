import os, re, json
from pathlib import Path
from typing import List
from docx import Document as DocxDocument
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()

STANDARDS_DIR = Path("standards")
INDEX_DIR = Path("standards_index")
INDEX_DIR.mkdir(exist_ok=True)

def read_txt(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")

def read_docx(path: Path) -> str:
    doc = DocxDocument(path)
    return "\n".join(p.text for p in doc.paragraphs)

def read_pdf(path: Path) -> str:
    # Minimal PDF text extractor without extra deps:
    # If your PDFs don’t extract well, consider installing "pypdf".
    try:
        from pypdf import PdfReader
        reader = PdfReader(str(path))
        return "\n".join(page.extract_text() or "" for page in reader.pages)
    except Exception:
        # fallback (empty) – recommend installing pypdf: python -m pip install pypdf
        return ""

def load_file(path: Path) -> str:
    if path.suffix.lower() == ".txt":
        return read_txt(path)
    if path.suffix.lower() == ".docx":
        return read_docx(path)
    if path.suffix.lower() == ".pdf":
        return read_pdf(path)
    return ""

def chunk_text(text: str, max_len=1500, overlap=150) -> List[str]:
    # simple paragraph-based chunker
    paras = [p.strip() for p in re.split(r"\n{2,}", text) if p.strip()]
    chunks, cur = [], ""
    for p in paras:
        if len(cur) + len(p) + 2 <= max_len:
            cur = f"{cur}\n\n{p}" if cur else p
        else:
            if cur: chunks.append(cur)
            # start new with some overlap
            cur = p[:max_len]
    if cur: chunks.append(cur)
    # add small overlap between chunks
    if overlap and len(chunks) > 1:
        with_overlap = []
        for i, ch in enumerate(chunks):
            if i == 0:
                with_overlap.append(ch)
            else:
                prev = chunks[i-1]
                tail = prev[-overlap:]
                with_overlap.append(tail + "\n" + ch)
        chunks = with_overlap
    return chunks

def embed(texts: List[str]) -> List[List[float]]:
    # uses OpenAI embeddings (private, local index)
    resp = client.embeddings.create(
        model="text-embedding-3-large",
        input=texts
    )
    return [d.embedding for d in resp.data]

def main():
    records = []
    for path in STANDARDS_DIR.iterdir():
        if not path.is_file(): continue
        content = load_file(path)
        if not content: 
            print(f"Skipped (unreadable): {path.name}")
            continue
        chunks = chunk_text(content)
        print(f"Ingesting {path.name} → {len(chunks)} chunks")
        embs = embed(chunks)
        for i, (ch, vec) in enumerate(zip(chunks, embs)):
            records.append({
                "source": path.name,
                "chunk_id": f"{path.name}::chunk{i}",
                "text": ch,
                "embedding": vec
            })

    # save as JSONL (simple local “vector store”)
    out_path = INDEX_DIR / "standards_index.jsonl"
    with out_path.open("w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r) + "\n")
    print(f"Indexed {len(records)} chunks → {out_path}")

if __name__ == "__main__":
    main()
