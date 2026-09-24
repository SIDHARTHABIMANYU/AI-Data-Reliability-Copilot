from backend.services.pinecone_service import (
    search_documents,
    build_context,
    build_rag_prompt
)


def create_rag_prompt(query: str) -> str:

    try:

        results = search_documents(query)

        if not results.matches:

            return (
                "The knowledge base does not contain relevant information "
                "to answer this question."
            )

        context = build_context(results)

        prompt = build_rag_prompt(query, context)

        return prompt

    except Exception:

        return (
            "I couldn't retrieve the relevant information from "
            "the knowledge base."
        )