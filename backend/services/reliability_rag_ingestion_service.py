from pathlib import Path
import os

from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain_text_splitters import RecursiveCharacterTextSplitter

from backend.config.settings import settings


BASE_DIR = Path(__file__).resolve().parent.parent.parent
KNOWLEDGE_BASE_DIR = BASE_DIR / "knowledge_base"

RELIABILITY_DOCUMENTS = [
    "data_contracts.txt",
    "pipeline_runbooks.txt",
    "business_metrics.txt",
    "incident_procedures.txt",
    "remediation_guidelines.txt",
]

NAMESPACE = "reliability"


os.environ["PINECONE_API_KEY"] = settings.PINECONE_API_KEY


embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100,
)


def load_reliability_documents() -> list[Document]:
    documents = []

    for filename in RELIABILITY_DOCUMENTS:
        file_path = KNOWLEDGE_BASE_DIR / filename

        if not file_path.exists():
            raise FileNotFoundError(
                f"Reliability knowledge file not found: {file_path}"
            )

        content = file_path.read_text(encoding="utf-8")

        documents.append(
            Document(
                page_content=content,
                metadata={
                    "source": filename,
                    "knowledge_type": "reliability",
                },
            )
        )

    return documents


def ingest_reliability_documents() -> None:
    documents = load_reliability_documents()

    chunks = text_splitter.split_documents(documents)

    PineconeVectorStore.from_documents(
        documents=chunks,
        embedding=embeddings,
        index_name="business-ai",
        namespace=NAMESPACE,
    )

    print("Reliability knowledge ingestion completed.")
    print(f"Documents loaded: {len(documents)}")
    print(f"Chunks created: {len(chunks)}")
    print(f"Pinecone namespace: {NAMESPACE}")

    print("\nSources:")

    for document in documents:
        print(f"- {document.metadata['source']}")


if __name__ == "__main__":
    ingest_reliability_documents()