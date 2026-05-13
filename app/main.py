from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.rag import answer_question
from app.schemas import AnswerResponse, QuestionRequest

app = FastAPI(
    title="MedReg MCP",
    description="Healthcare AI documentation agent with cited RAG over FDA and WHO sources",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/ask", response_model=AnswerResponse)
async def ask(request: QuestionRequest):
    return await answer_question(request.question)
