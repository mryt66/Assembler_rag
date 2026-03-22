import json
from pathlib import Path
from typing import Any
import fitz
from google import genai
from pydantic import BaseModel
from config.config import settings


def extract_pdf_text(filename: str) -> str:
    text = ""
    with fitz.open(filename) as doc:
        for page in doc:
            text += page.get_text()
    return text


def chunk_pdf(filename: str) -> list[dict[str, Any]]:
    api_key = settings.gemini_api_key
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY not set")

    client = genai.Client(api_key=api_key)
    text = extract_pdf_text(filename)
    pdf_name = Path(filename).name

    prompt = f"""
    Split the following text into coherent chunks suitable for RAG.
    Each chunk should be 100-500 words.
    Do not cut mid-sentence, paragraph, or table.
    Preserve headings, bullet points, and tables.

    Return an array of JSON objects with this structure:
    {{
        "content": "<chunk text>",
        "source": "{pdf_name}",
        "tags": [],
        "type": "prg"
    }}
    Text:
    {text}
    """

    response = client.models.generate_content(
        model=settings.gemini_model,
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "response_schema": settings.response_schema,
        },
    )

    parsed = response.parsed
    chunks: list[dict[str, Any]] = [
        c.model_dump() if isinstance(c, BaseModel) else c for c in (parsed or [])
    ]
    return chunks


def process_pdf_folder(folder_path: str | Path) -> list[dict[str, Any]]:
    folder = Path(folder_path)
    pdfs = sorted(folder.glob("*.pdf"), key=lambda x: x.name)
    if not pdfs:
        print(f"No PDF files found in {folder_path}")
        return []
    all_chunks = []
    for pdf_file in pdfs:
        print(f"Processing PDF: {pdf_file.name}")
        chunks = chunk_pdf(filename=str(pdf_file))
        all_chunks.extend(chunks)
    return all_chunks


def make_prg_chunk(text: str, filename: str | Path) -> list[dict[str, Any]]:
    return [
        {
            "content": text.strip(),
            "source": Path(filename).name,
            "tags": [],
            "type": "prg",
        }
    ]


def process_prg_folder(folder_path: str | Path) -> list[dict[str, Any]]:
    folder = Path(folder_path)
    prgs = sorted(folder.glob("*.prg"), key=lambda x: x.name)
    if not prgs:
        print(f"No .prg files found in {folder_path}")
        return []
    all_chunks = []
    for prg_file in prgs:
        print(f"Processing PRG: {prg_file.name}")
        text = prg_file.read_text(encoding="utf-8", errors="ignore")
        chunk = make_prg_chunk(text, prg_file.name)
        all_chunks.extend(chunk)
    return all_chunks


def main() -> None:
    data_dir = settings.data_dir
    pdf_folder = data_dir / "pdfs"
    prg_folder = data_dir / "prg"
    output_jsonl = settings.output_chunks_file

    all_chunks = process_pdf_folder(pdf_folder)
    all_chunks += process_prg_folder(prg_folder)

    with open(output_jsonl, "w", encoding="utf-8") as f:
        json.dump(all_chunks, f, ensure_ascii=False, indent=2)

    print(f"Finished. {len(all_chunks)} total chunks written to {output_jsonl}")


if __name__ == "__main__":
    main()
