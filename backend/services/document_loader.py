from pathlib import Path


KNOWLEDGE_BASE_DIR = Path("knowledge_base")


def clean_text(text: str) -> str:

    lines = text.splitlines()

    cleaned_lines = []

    for line in lines:

        line = line.strip()

        if line:
            cleaned_lines.append(line)

    return "\n".join(cleaned_lines)


def load_documents():

    documents = []

    for file_path in KNOWLEDGE_BASE_DIR.glob("*.txt"):

        text = file_path.read_text(encoding="utf-8")

        text = clean_text(text)

        documents.append({
            "text": text,
            "source": file_path.name
        })

    return documents