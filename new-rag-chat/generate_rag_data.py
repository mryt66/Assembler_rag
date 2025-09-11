import google.generativeai as genai
from typing import List
from pathlib import Path
import fitz
import json
from config import Chunk, Settings


def extract_pdf_text(filename: str) -> str:
    text = ""
    with fitz.open(filename) as doc:
        for page in doc:
            text += page.get_text()
    return text


def chunk_pdf(filename: str) -> List[Chunk]:
    client = genai.Client()
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

    client = genai.Client()
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "response_schema": Settings.response_schema,
        },
    )

    chunks: List[Chunk] = response.parsed
    return chunks


def process_pdf_folder(folder_path):
    folder = Path(folder_path)
    pdfs = list(folder.glob("*.pdf"))
    all_chunks = []
    if not pdfs:
        print(f"No PDF files found in {folder_path}")
        return []
    else:
        pdfs.sort(key=lambda x: x.name)
        for pdf_file in pdfs:
            print(f"Processing PDF: {pdf_file.name}")
            chunks = chunk_pdf(filename=pdf_file)
            all_chunks.extend(chunks)
    return all_chunks


def make_prg_chunk(text, filename):
    return [
        {
            "content": text.strip(),
            "source": Path(filename).name,
            "tags": [],
            "type": "prg",
        }
    ]


def process_prg_folder(folder_path):
    folder = Path(folder_path)
    all_chunks = []
    prgs = list(folder.glob("*.prg"))
    if not prgs:
        print(f"No .prg files found in {folder_path}")
        return []
    prgs.sort(key=lambda x: x.name)
    for prg_file in prgs:
        print(f"Processing PRG: {prg_file.name}")
        text = prg_file.read_text(encoding="utf-8", errors="ignore")
        chunk = make_prg_chunk(text, prg_file.name)
        all_chunks.extend(chunk)
    return all_chunks


def main():
    # Use project-relative data folders
    base_dir = Path(__file__).resolve().parent
    data_dir = base_dir / "data"
    pdf_folder = data_dir / "pdfs"
    prg_folder = data_dir / "prg"
    output_jsonl = base_dir / "output_chunks.jsonl"  # keep root location for now

    all_chunks = process_pdf_folder(pdf_folder)

    if prg_folder:
        all_chunks += process_prg_folder(prg_folder)

    with open(output_jsonl, "w", encoding="utf-8") as f:
        json.dump(all_chunks, f, ensure_ascii=False, indent=2)

    print(f"Finished. {len(all_chunks)} total chunks written to {output_jsonl}")


if __name__ == "__main__":
    main()
