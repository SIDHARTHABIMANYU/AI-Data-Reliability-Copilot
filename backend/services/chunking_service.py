def chunk_text(
    text: str,
    chunk_size: int = 80,
    chunk_overlap: int = 1
) -> list[str]:

    paragraphs = [
        paragraph.strip()
        for paragraph in text.split("\n\n")
        if paragraph.strip()
    ]

    chunks = []

    for paragraph in paragraphs:

        words = paragraph.split()

        for i in range(0, len(words), chunk_size):

            chunk = " ".join(
                words[i:i + chunk_size]
            )

            if chunk:
                chunks.append(chunk)

    return chunks

from backend.services.document_loader import load_documents


def chunk_documents():

    documents = load_documents()

    all_chunks = []

    for document in documents:

        chunks = chunk_text(
            document["text"],
            chunk_size=50,
            chunk_overlap=10
        )

        for chunk in chunks:

            all_chunks.append({
                "text": chunk,
                "source": document["source"]
            })

    return all_chunks
