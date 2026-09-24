from backend.services.chunking_service import chunk_documents
from backend.services.pinecone_service import ingest_chunks


def ingest_knowledge_base():

    chunks = chunk_documents()

    ingest_chunks(chunks)

    print(f"Successfully ingested {len(chunks)} chunks.")


if __name__ == "__main__":
    ingest_knowledge_base()