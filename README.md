# Business-AI

> A GenAI business assistant, currently in progress, built with FastAPI, AWS Bedrock, LangChain, Pinecone, and Retrieval-Augmented Generation (RAG).

Business-AI is an AI-powered business assistant designed to answer business-related questions using a controlled knowledge base instead of relying only on the language model's internal knowledge.

The project started as a basic AWS Bedrock chatbot and has evolved through multiple engineering stages into a structured RAG application with FastAPI, Pinecone vector search, LangChain, semantic retrieval, relevance filtering, source attribution, and automated tests.

## Project Evolution

- V1: Basic Bedrock chatbot
- V2: Production-style GenAI API
- V3: RAG with Pinecone and LangChain

## Architecture

User query → FastAPI backend → LangChain retrieval → Pinecone (semantic search over the knowledge base) → AWS Bedrock (grounded answer generation) → response with sources

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python, FastAPI, Pydantic |
| LLM | AWS Bedrock |
| Orchestration | LangChain |
| Vector Database | Pinecone |
| Testing | Pytest |

## Key Features

- Answers grounded in a controlled knowledge base instead of the model's internal knowledge
- Semantic retrieval with relevance filtering
- Source attribution on responses
- Automated tests

## Setup

Clone the repo, install dependencies from requirements.txt, add your AWS Bedrock credentials and Pinecone API key to a local .env file (never commit it), then start the FastAPI backend from the backend folder.

## Status

Actively in development.
