import tiktoken


def _get_encoder():
    return tiktoken.get_encoding("cl100k_base")


def count_tokens(text: str) -> int:
    encoder = _get_encoder()
    return len(encoder.encode(text))


def chunk_text(text: str, chunk_size: int = 800, chunk_overlap: int = 100) -> list[str]:
    if not text or not text.strip():
        return []

    encoder = _get_encoder()

    paragraphs = text.split("\n\n")
    if len(paragraphs) == 1:
        paragraphs = text.split("\n")

    chunks = []
    current_chunk = []
    current_tokens = 0

    for paragraph in paragraphs:
        paragraph = paragraph.strip()
        if not paragraph:
            continue

        para_tokens = len(encoder.encode(paragraph))

        if para_tokens > chunk_size:
            if current_chunk:
                chunks.append("\n\n".join(current_chunk))
                current_chunk = []
                current_tokens = 0

            sentences = _split_into_sentences(paragraph)
            for sentence in sentences:
                sent_tokens = len(encoder.encode(sentence))
                if current_tokens + sent_tokens > chunk_size and current_chunk:
                    chunks.append(" ".join(current_chunk))
                    overlap_text = " ".join(current_chunk)
                    overlap_tokens = encoder.encode(overlap_text)
                    if len(overlap_tokens) > chunk_overlap:
                        overlap_decoded = encoder.decode(overlap_tokens[-chunk_overlap:])
                        current_chunk = [overlap_decoded]
                        current_tokens = chunk_overlap
                    else:
                        current_chunk = [overlap_text]
                        current_tokens = len(overlap_tokens)
                current_chunk.append(sentence)
                current_tokens += sent_tokens
            continue

        if current_tokens + para_tokens > chunk_size and current_chunk:
            chunks.append("\n\n".join(current_chunk))
            overlap_text = "\n\n".join(current_chunk)
            overlap_tokens = encoder.encode(overlap_text)
            if len(overlap_tokens) > chunk_overlap:
                overlap_decoded = encoder.decode(overlap_tokens[-chunk_overlap:])
                current_chunk = [overlap_decoded]
                current_tokens = chunk_overlap
            else:
                current_chunk = [overlap_text]
                current_tokens = len(overlap_tokens)
        else:
            current_chunk.append(paragraph)
            current_tokens += para_tokens

    if current_chunk:
        chunks.append("\n\n".join(current_chunk))

    return chunks


def _split_into_sentences(text: str) -> list[str]:
    import re

    sentences = re.split(r"(?<=[.!?])\s+", text)
    return [s.strip() for s in sentences if s.strip()]
