from app.rag import answer_question
from app.schemas import AnswerResponse

TOOL_NAME = "query_healthcare_ai_docs"
TOOL_DESCRIPTION = (
    "Search FDA and WHO public documentation about healthcare AI regulation, "
    "responsible AI practices, and medical device software guidance. "
    "Returns a cited answer grounded in official sources. "
    "Do NOT use this tool for medical advice - it only covers regulatory and governance documentation."
)


async def handle_query(question: str) -> str:
    response: AnswerResponse = await answer_question(question)

    output = response.answer

    if response.citations:
        output += "\n\n---\nSources:\n"
        for i, citation in enumerate(response.citations, start=1):
            output += f"[{i}] {citation.source_title}\n    {citation.source_url}\n"

    return output
