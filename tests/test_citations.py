from app.citations import extract_citations
from app.schemas import Citation


def _make_citations(n: int) -> list[Citation]:
    return [
        Citation(
            source_title=f"Source {i}",
            source_url=f"https://example.com/doc{i}",
            snippet=f"Snippet from source {i}",
        )
        for i in range(1, n + 1)
    ]


class TestExtractCitations:
    def test_single_citation(self):
        citations = _make_citations(3)
        answer = "According to the FDA guidance [1], AI devices require validation."
        result = extract_citations(answer, citations)
        assert len(result) == 1
        assert result[0].source_title == "Source 1"

    def test_multiple_citations(self):
        citations = _make_citations(5)
        answer = "Both FDA [1] and WHO [3] recommend governance frameworks [5]."
        result = extract_citations(answer, citations)
        assert len(result) == 3
        assert result[0].source_title == "Source 1"
        assert result[1].source_title == "Source 3"
        assert result[2].source_title == "Source 5"

    def test_no_citations_in_answer(self):
        citations = _make_citations(3)
        answer = "AI in healthcare requires careful governance."
        result = extract_citations(answer, citations)
        assert len(result) == 0

    def test_out_of_range_citation_ignored(self):
        citations = _make_citations(3)
        answer = "This references [4] and [10] which don't exist, plus [2] which does."
        result = extract_citations(answer, citations)
        assert len(result) == 1
        assert result[0].source_title == "Source 2"

    def test_duplicate_citations_deduplicated(self):
        citations = _make_citations(3)
        answer = "As stated in [1] and further confirmed [1] by the FDA."
        result = extract_citations(answer, citations)
        assert len(result) == 1

    def test_numbers_not_in_brackets_ignored(self):
        citations = _make_citations(3)
        answer = "There are 3 key principles and 2 main concerns."
        result = extract_citations(answer, citations)
        assert len(result) == 0
