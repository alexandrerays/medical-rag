from pydantic import BaseModel


class QuestionRequest(BaseModel):
    question: str


class Citation(BaseModel):
    source_title: str
    source_url: str
    snippet: str


class AnswerResponse(BaseModel):
    answer: str
    citations: list[Citation]
    safety_triggered: bool


class ChunkMetadata(BaseModel):
    title: str
    url: str
    source_org: str
    chunk_index: int
