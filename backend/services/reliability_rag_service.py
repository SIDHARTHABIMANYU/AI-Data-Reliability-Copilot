import os

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_pinecone import PineconeVectorStore

from backend.config.settings import settings


os.environ["PINECONE_API_KEY"] = settings.PINECONE_API_KEY


NAMESPACE = "reliability"
TOP_K = 4
RELEVANCE_THRESHOLD = 0.3


embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


vector_store = PineconeVectorStore(
    index_name="business-ai",
    embedding=embeddings,
    namespace=NAMESPACE,
    pinecone_api_key=settings.PINECONE_API_KEY,
)


def retrieve_reliability_context(query: str) -> str:
    results = vector_store.similarity_search_with_score(
        query,
        k=TOP_K,
    )

    relevant_results = [
        (document, score)
        for document, score in results
        if score >= RELEVANCE_THRESHOLD
    ]

    if not relevant_results:
        return ""

    context_parts = []

    for document, score in relevant_results:
        source = document.metadata.get(
            "source",
            "Unknown"
        )

        context_parts.append(
            f"Source: {source}\n"
            f"Relevance Score: {score:.3f}\n"
            f"Content:\n{document.page_content}"
        )

    return "\n\n---\n\n".join(context_parts)


if __name__ == "__main__":

    query = (
        "What should we do when the sales dataset "
        "has a schema change from sales_amount to another column?"
    )

    results = retrieve_reliability_context(query)

    print("\nRetrieved Reliability Context:\n")
    print(results)