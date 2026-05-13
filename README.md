# MedReg MCP

A healthcare AI documentation agent that helps technical and product teams answer questions about responsible AI in regulated medical contexts, using cited retrieval over public FDA and WHO documentation.

It exposes the same knowledge base through both **FastAPI** and an **MCP server** so it can be used by applications and Claude-compatible clients.

> **Note:** This is NOT a medical diagnosis or treatment tool. It is a regulatory and responsible AI documentation assistant.

## Architecture

```
┌─────────────────┐     ┌──────────────┐     ┌───────────────┐
│  FastAPI /ask   │────▶│   RAG Engine │────▶│ Anthropic API │
└─────────────────┘     │              │     └───────────────┘
                        │  - Safety    │
┌─────────────────┐     │  - Embed     │     ┌───────────────┐
│  MCP Server     │────▶│  - Search    │────▶│   Supabase    │
│  (stdio)        │     │  - Cite      │     │   pgvector    │
└─────────────────┘     └──────────────┘     └───────────────┘
                              ▲
                              │
                   ┌──────────────────┐
                   │ Ingestion Pipeline│
                   │ (crawl/chunk/embed)│
                   └──────────────────┘
```

## Setup

### 1. Prerequisites

- Python 3.11+
- Supabase project with pgvector enabled
- Anthropic API key
- Voyage AI API key (for embeddings)

### 2. Install Dependencies

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Configure Environment

```bash
cp .env.example .env
# Edit .env with your API keys and Supabase credentials
```

### 4. Set Up Database

Run the SQL in `scripts/setup_db.sql` in your Supabase SQL editor to create the `documents` table and similarity search function.

### 5. Ingest Documents

```bash
python -m ingestion.ingest
```

This crawls FDA and WHO pages, chunks the text, generates embeddings, and stores everything in Supabase.

## Usage

### FastAPI Server

```bash
uvicorn app.main:app --reload
```

Query the API:

```bash
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What does FDA say about AI/ML-enabled medical devices?"}'
```

Response:

```json
{
  "answer": "According to FDA guidance...[1][2]",
  "citations": [
    {
      "source_title": "AI/ML-Enabled Medical Devices",
      "source_url": "https://www.fda.gov/...",
      "snippet": "..."
    }
  ],
  "safety_triggered": false
}
```

### MCP Server

Connect from Claude Desktop by adding to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "medreg": {
      "command": "python",
      "args": ["-m", "mcp_server.server"],
      "cwd": "/path/to/medical-rag"
    }
  }
}
```

The server exposes one tool: `query_healthcare_ai_docs`

## Evaluation

Run the evaluation suite (15 Q&A pairs testing citation quality, safety, keyword recall, and source accuracy):

```bash
python -m evals.run_eval
```

## Tests

```bash
pytest tests/ -v
```

## Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Embedding model | Voyage `voyage-3-lite` (1024d) | Recommended for RAG, good cost/quality balance |
| Chunk size | 800 tokens, 100 overlap | Preserves regulatory context without noise |
| Top-k | 5 | Sufficient diversity for multi-faceted questions |
| Citation format | Inline `[1]`, `[2]` with source list | Familiar, parseable, verifiable |
| Safety | Regex patterns | Fast, deterministic, no extra LLM cost |
| MCP transport | stdio | Standard for local MCP servers |
| Vector store | Supabase + pgvector | Managed, scalable, good DX |

## Production Considerations

If deploying this to production, I would additionally:

- Add rate limiting and authentication to the FastAPI endpoint
- Implement caching for repeated queries (embedding + search results)
- Add monitoring/observability (latency, token usage, safety trigger rate)
- Set up periodic re-ingestion as FDA/WHO documents update
- Add a feedback loop to improve retrieval quality
- Consider hybrid search (keyword + vector) for better recall
- Add request tracing for debugging citation quality issues
- Deploy the MCP server as an SSE endpoint for remote access
