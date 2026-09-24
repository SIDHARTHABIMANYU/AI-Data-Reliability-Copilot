from backend.services.pinecone_service import search_documents
from backend.services.rag_service import create_rag_prompt


def test_business_models_retrieval():

    results = search_documents(
        "What are common business models?"
    )

    assert len(results.matches) > 0

    retrieved_text = " ".join(
        match.metadata["text"]
        for match in results.matches
    )

    assert "subscription" in retrieved_text.lower()
    assert "marketplace" in retrieved_text.lower()


def test_customer_segmentation_retrieval():

    results = search_documents(
        "What is customer segmentation?"
    )

    assert len(results.matches) > 0

    retrieved_text = " ".join(
        match.metadata["text"]
        for match in results.matches
    )

    assert "customer segmentation" in retrieved_text.lower()


def test_unrelated_question():

    results = search_documents(
        "What is the capital of France?"
    )

    assert len(results.matches) == 0


def test_rag_prompt_contains_retrieved_context():

    prompt = create_rag_prompt(
        "What are common business models?"
    )

    assert "subscription" in prompt.lower()
    assert "marketplace" in prompt.lower()