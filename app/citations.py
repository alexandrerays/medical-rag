import re

from app.schemas import Citation


def format_context(chunks: list[dict]) -> tuple[list[str], list[Citation]]:
    from app.prompts import format_context_block

    context_blocks = []
    citations = []

    for i, chunk in enumerate(chunks, start=1):
        metadata = chunk["metadata"]
        block = format_context_block(
            index=i,
            title=metadata["title"],
            org=metadata["source_org"],
            url=metadata["url"],
            content=chunk["content"],
        )
        context_blocks.append(block)

        snippet = chunk["content"][:200] + "..." if len(chunk["content"]) > 200 else chunk["content"]
        citations.append(
            Citation(
                source_title=metadata["title"],
                source_url=metadata["url"],
                snippet=snippet,
            )
        )

    return context_blocks, citations


def extract_citations(answer: str, available_citations: list[Citation]) -> list[Citation]:
    referenced_indices = set()
    for match in re.finditer(r"\[(\d+)\]", answer):
        idx = int(match.group(1))
        if 1 <= idx <= len(available_citations):
            referenced_indices.add(idx - 1)

    return [available_citations[i] for i in sorted(referenced_indices)]
