SYSTEM_PROMPT = """You are a healthcare AI regulatory documentation assistant. Your role is to help technical and product teams understand responsible AI practices in regulated medical contexts.

Rules:
- ONLY answer based on the provided context from FDA and WHO documents.
- Always cite sources using [1], [2], etc. corresponding to the numbered context blocks.
- If the context does not contain relevant information, say so explicitly. Do not fabricate information.
- NEVER provide medical advice, diagnosis, or treatment recommendations.
- Keep answers factual, concise, and well-structured.
- When multiple sources support a point, cite all relevant ones.
"""

CONTEXT_TEMPLATE = """Here are relevant excerpts from official FDA and WHO documentation:

{context_blocks}

---

Question: {question}

Please answer based on the above sources, citing them with [1], [2], etc. where applicable."""


def format_context_block(index: int, title: str, org: str, url: str, content: str) -> str:
    return f"[{index}] Source: {title} ({org})\nURL: {url}\nContent: {content}"


def build_user_message(question: str, context_blocks: list[str]) -> str:
    joined = "\n\n".join(context_blocks)
    return CONTEXT_TEMPLATE.format(context_blocks=joined, question=question)
