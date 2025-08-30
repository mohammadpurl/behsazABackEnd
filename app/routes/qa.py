from fastapi import APIRouter
from app.schemas.qa_schema import QuestionRequest, AnswerResponse
from app.services.vercel_rag_service import answer_question

router = APIRouter()


@router.post("/query", response_model=AnswerResponse)
async def query_qa(request: QuestionRequest):
    answer = answer_question(request.question)
    return AnswerResponse(question=request.question, answer=answer)
