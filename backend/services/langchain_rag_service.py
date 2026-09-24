from langchain_huggingface import HuggingFaceEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain_aws import ChatBedrockConverse

from backend.config.settings import settings


RELEVANCE_THRESHOLD = 0.3

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


vector_store = PineconeVectorStore(
    index_name="business-ai",
    embedding=embeddings,
    pinecone_api_key=settings.PINECONE_API_KEY
)


retriever = vector_store.as_retriever(
    search_kwargs={
        "k": 2
    }
)


llm = ChatBedrockConverse(
    model=settings.BEDROCK_MODEL_ID,
    region_name=settings.AWS_REGION,
    max_tokens=500,
    temperature=0.7
)


def retrieve_context(query: str) -> str:

    results = vector_store.similarity_search_with_score(
        query,
        k=2
    )

    context_parts = []

    for doc, score in results:

        if score < 0.3:
            continue

        source = doc.metadata.get("source")

        context_parts.append(
            f"Source: {source}\n"
            f"Content: {doc.page_content}"
        )

    return "\n\n".join(context_parts)


def generate_answer(query: str, context: str) -> str:

    prompt = f"""
Use the following context to answer the user's question.

Context:
{context}

User Question:
{query}

Answer only using the provided context.
If the context does not contain enough information, say so clearly.
"""

    response = llm.invoke(prompt)

    return response.content

def generate_rag_answer(query: str) -> str:

    results = vector_store.similarity_search_with_score(
        query,
        k=2
    )

    relevant_docs = [
        (doc, score)
        for doc, score in results
        if score >= RELEVANCE_THRESHOLD
    ]

    if not relevant_docs:

        return (
            "The knowledge base does not contain relevant "
            "information to answer this question."
        )

    context_parts = []
    sources = set()

    for doc, score in relevant_docs:

        source = doc.metadata.get("source", "Unknown")

        sources.add(source)

        context_parts.append(
            f"Source: {source}\n"
            f"Content: {doc.page_content}"
        )

    context = "\n\n".join(context_parts)

    answer = generate_answer(
        query=query,
        context=context
    )

    source_text = "\n".join(
        f"- {source}"
        for source in sorted(sources)
    )

    return (
        f"{answer}\n\n"
        f"**Sources:**\n"
        f"{source_text}"
    )