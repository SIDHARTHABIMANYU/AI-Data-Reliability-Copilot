from pinecone import Pinecone

from backend.config.settings import settings
from backend.services.embedding_service import create_embedding


pc = Pinecone(
    api_key=settings.PINECONE_API_KEY
)

index = pc.Index("business-ai")


def ingest_chunks(chunks):

    for i, chunk in enumerate(chunks):

        embedding = create_embedding(chunk["text"])

        source = chunk["source"]

        vector_id = f"{source}-{i}"

        index.upsert(
            vectors=[
                {
                    "id": vector_id,
                    "values": embedding,
                    "metadata": {
                        "text": chunk["text"],
                        "source": source,
                        "chunk_index": i
                    }
                }
            ]
        )


def search_documents(
    query: str,
    top_k: int = 3,
    score_threshold: float = 0.3
):

    query_embedding = create_embedding(query)

    results = index.query(
        vector=query_embedding,
        top_k=top_k,
        include_metadata=True
    )

    filtered_matches = [
        match
        for match in results.matches
        if match.score >= score_threshold
    ]

    results.matches = filtered_matches

    return results


def build_context(results) -> str:

    context_parts = []

    for match in results.matches:

        text = match.metadata.get("text")
        source = match.metadata.get("source")

        if text:

            context_parts.append(
                f"Source: {source}\n"
                f"Content: {text}"
            )

    return "\n\n".join(context_parts)


def build_rag_prompt(
    query: str,
    context: str
) -> str:

    return f"""
Use the following context to answer the user's question.

Context:
{context}

User Question:
{query}

Answer based on the provided context.
"""