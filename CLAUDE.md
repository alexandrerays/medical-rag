# CLAUDE.md

## Project Overview

Build a technical assessment project for a Senior AI Builder role.

The application is called **MedReg MCP**.

MedReg MCP is a cited RAG agent over public healthcare AI documentation from **FDA** and **WHO**. The goal is to answer questions about responsible AI, digital health, AI/ML-enabled medical software, and regulatory considerations in healthcare AI.

The project must demonstrate:

1. Public documentation ingestion
2. Vector search with Supabase + pgvector
3. Cited question answering
4. FastAPI endpoint
5. MCP server integration
6. Simple but meaningful evaluation
7. Clear production-oriented tradeoff thinking

The application must not provide medical advice. It should answer questions about documentation, regulation, responsible AI, software validation, governance, and healthcare AI implementation.

---

## Assessment Requirements

The technical assessment asks for a working AI agent that answers questions over a public documentation site.

The required functionality is:

- Ingest public documentation into a vector store
- Prefer Supabase + pgvector
- Answer questions with proper citations back to the source
- Expose the Q&A through a small FastAPI endpoint
- Include evaluation with 10 to 15 question/answer pairs
- Choose one deeper option

For this project, the deeper option is:

**Option C: MCP Server**

The MCP server must expose the knowledge base as a tool any Claude-compatible client can connect to, with proper tool definitions, clear input/output schema, and a short demo.

---

## Product Framing

Frame the project as:

> A healthcare AI documentation agent that helps technical and product teams answer questions about responsible AI in regulated medical contexts, using cited retrieval over public FDA and WHO documentation. It exposes the same knowledge base through both FastAPI and an MCP server so it can be used by applications and Claude-compatible clients.

Important positioning:

- This is not a medical diagnosis or treatment tool.
- This is a regulatory and responsible AI documentation assistant.
- The goal is to support product, engineering, compliance, and AI teams.
- All answers must be grounded in FDA and WHO public sources.
- Answers must include citations whenever possible.

---

## Core Use Cases

The system should answer questions like:

- What are the main risks when deploying AI in healthcare?
- What should teams consider before using generative AI in clinical workflows?
- How should AI/ML-enabled medical software be evaluated?
- What does responsible AI mean in healthcare?
- What does WHO recommend for ethical AI in health?
- What does FDA say about AI/ML-enabled medical devices?
- What documentation should a team prepare before validating an AI healthcare product?
- How should teams think about model updates in AI/ML medical software?
- Can this tool decide a patient’s treatment?
- What are common governance practices for AI in healthcare?

For medical advice questions, the system should safely redirect:

Example:

User asks:

> Should this patient receive treatment A or treatment B?

The system should answer:

> I cannot provide medical advice or treatment recommendations. I can help summarize FDA or WHO documentation about responsible AI, software validation, risk management, and governance in healthcare AI systems.

---

## Recommended Tech Stack

Use the following stack:

- Python 3.11+
- FastAPI
- Uvicorn
- Supabase
- pgvector
- Anthropic Claude API
- MCP Python SDK
- BeautifulSoup or simple HTML loader
- Requests or httpx
- Pydantic
- python-dotenv
- pytest
- Optional: pandas for eval reporting

Do not over-engineer the project. Prioritize clarity, correctness, and a working demo.

---

## Documentation Sources

Use only FDA and WHO public documentation.

Recommended sources:

### FDA

Use public FDA pages related to:

- Artificial Intelligence and Machine Learning in Software as a Medical Device
- AI/ML-enabled medical devices
- Predetermined Change Control Plans
- Good Machine Learning Practice
- Software as a Medical Device where relevant

### WHO

Use public WHO pages or reports related to:

- Ethics and governance of artificial intelligence for health
- Regulatory considerations on artificial intelligence for health
- Digital health guidance
- Responsible use of AI in health

Keep ingestion simple. Use a small curated list of URLs instead of a broad crawler.

The crawler should:

- Fetch a list of predefined FDA and WHO URLs
- Extract title, text, and URL
- Split text into chunks
- Store chunks in Supabase with metadata

Avoid recursive crawling unless it can be implemented safely and quickly.

---

## Repository Structure

Use this structure:

```text
medreg-mcp/
  app/
    __init__.py
    main.py
    config.py
    schemas.py
    rag.py
    prompts.py
    citations.py
    safety.py
    vector_store.py
    embeddings.py
    llm.py

  ingestion/
    __init__.py
    sources.py
    crawler.py
    chunker.py
    ingest.py

  mcp_server/
    __init__.py
    server.py
    tools.py

  evals/
    eval_questions.json
    run_eval.py
    metrics.py

  scripts/
    setup_db.sql
    demo_queries.sh

  tests/
    test_safety.py
    test_chunking.py
    test_citations.py

  README.md
  CLAUDE.md
  requirements.txt
  .env.example
  .gitignore