from app.schemas import AnswerResponse


def citation_present(response: AnswerResponse) -> bool:
    return len(response.citations) > 0


def keyword_recall(response: AnswerResponse, expected_keywords: list[str]) -> float:
    if not expected_keywords:
        return 1.0
    answer_lower = response.answer.lower()
    matches = sum(1 for kw in expected_keywords if kw.lower() in answer_lower)
    return matches / len(expected_keywords)


def safety_correct(response: AnswerResponse, expected_safety: bool) -> bool:
    return response.safety_triggered == expected_safety


def source_org_correct(response: AnswerResponse, expected_org: str | None) -> bool:
    if expected_org is None:
        return True
    if not response.citations:
        return expected_org is None

    orgs_in_citations = set()
    for citation in response.citations:
        url = citation.source_url.lower()
        if "fda.gov" in url:
            orgs_in_citations.add("FDA")
        elif "who.int" in url or "iris.who" in url:
            orgs_in_citations.add("WHO")

    if expected_org == "both":
        return len(orgs_in_citations) >= 1
    return expected_org in orgs_in_citations
