from ingestion.chunker import chunk_text, count_tokens


class TestChunkText:
    def test_empty_text_returns_empty(self):
        assert chunk_text("") == []

    def test_whitespace_only_returns_empty(self):
        assert chunk_text("   \n\n  ") == []

    def test_short_text_returns_single_chunk(self):
        text = "This is a short paragraph about AI in healthcare."
        chunks = chunk_text(text)
        assert len(chunks) == 1
        assert text in chunks[0]

    def test_chunks_respect_size_limit(self):
        paragraphs = ["This is paragraph number {}. ".format(i) * 50 for i in range(20)]
        text = "\n\n".join(paragraphs)
        chunks = chunk_text(text, chunk_size=200, chunk_overlap=20)
        for chunk in chunks:
            token_count = count_tokens(chunk)
            assert token_count <= 250  # allow small overflow from overlap

    def test_multiple_paragraphs_produce_multiple_chunks(self):
        paragraphs = ["Paragraph {} about healthcare AI regulation. ".format(i) * 30 for i in range(10)]
        text = "\n\n".join(paragraphs)
        chunks = chunk_text(text, chunk_size=100, chunk_overlap=10)
        assert len(chunks) > 1

    def test_preserves_content(self):
        text = "Important FDA regulation about AI.\n\nWHO guidance on ethics."
        chunks = chunk_text(text)
        combined = " ".join(chunks)
        assert "FDA" in combined
        assert "WHO" in combined


class TestCountTokens:
    def test_empty_string(self):
        assert count_tokens("") == 0

    def test_simple_text(self):
        tokens = count_tokens("Hello world")
        assert tokens > 0
        assert tokens < 10
