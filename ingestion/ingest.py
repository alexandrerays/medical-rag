"""Ingestion pipeline: crawl sources, chunk, embed, and store in Supabase."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.embeddings import get_embeddings
from app.vector_store import upsert_documents
from ingestion.chunker import chunk_text
from ingestion.crawler import crawl_sources_sync
from ingestion.sources import SOURCES


def run_ingestion():
    print("Starting ingestion pipeline...")
    print(f"Sources to process: {len(SOURCES)}")

    print("\n[1/4] Crawling sources...")
    documents = crawl_sources_sync(SOURCES)
    print(f"  Successfully fetched {len(documents)} documents")

    if not documents:
        print("No documents fetched. Exiting.")
        return

    print("\n[2/4] Chunking documents...")
    all_chunks = []
    for doc in documents:
        chunks = chunk_text(doc["text"])
        for i, chunk_content in enumerate(chunks):
            all_chunks.append(
                {
                    "content": chunk_content,
                    "metadata": {
                        "title": doc["source_title"],
                        "url": doc["url"],
                        "source_org": doc["org"],
                        "chunk_index": i,
                    },
                }
            )
    print(f"  Total chunks: {len(all_chunks)}")

    print("\n[3/4] Generating embeddings...")
    texts = [chunk["content"] for chunk in all_chunks]
    embeddings = get_embeddings(texts)
    print(f"  Generated {len(embeddings)} embeddings")

    print("\n[4/4] Upserting to Supabase...")
    records = []
    for chunk, embedding in zip(all_chunks, embeddings):
        records.append(
            {
                "content": chunk["content"],
                "metadata": chunk["metadata"],
                "embedding": embedding,
            }
        )
    upsert_documents(records)
    print(f"  Upserted {len(records)} records")

    print("\nIngestion complete!")


if __name__ == "__main__":
    run_ingestion()
