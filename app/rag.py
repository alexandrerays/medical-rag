from app.citations import extract_citations, format_context
from app.config import get_settings
from app.embeddings import get_embedding
from app.llm import generate_answer
from app.prompts import SYSTEM_PROMPT, build_user_message
from app.safety import get_safety_response, is_medical_advice_request
from app.schemas import AnswerResponse
from app.vector_store import search


async def answer_question(question: str) -> AnswerResponse:
    if is_medical_advice_request(question):
        return AnswerResponse(
            answer=get_safety_response(),
            citations=[],
            safety_triggered=True,
        )

    settings = get_settings()

    query_embedding = get_embedding(question)

    results = search(query_embedding, top_k=settings.top_k)

    if not results:
        return AnswerResponse(
            answer="I could not find relevant information in the FDA or WHO documentation to answer this question.",
            citations=[],
            safety_triggered=False,
        )

    context_blocks, available_citations = format_context(results)
    user_message = build_user_message(question, context_blocks)

    answer_text = await generate_answer(question, user_message, SYSTEM_PROMPT)

    referenced_citations = extract_citations(answer_text, available_citations)

    return AnswerResponse(
        answer=answer_text,
        citations=referenced_citations,
        safety_triggered=False,
    )
