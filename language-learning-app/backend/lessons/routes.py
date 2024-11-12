from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from fastapi.concurrency import run_in_threadpool
from sqlmodel import Session
from database import get_session, supabase
from pydantic import BaseModel
from models import Difficulty, Language, Question, QuestionType
from langchain.generate_questions import generate_question
# from models import User

SessionDep = Annotated[Session, Depends(get_session)]

router = APIRouter()

@router.post("/generate")
async def generate_store_question(
    language: str,
    difficulty: str,
    question_type: str,
    session: SessionDep
) -> Question:
    
    question_data = await run_in_threadpool(generate_question, {
        "language": language,
        "difficulty": difficulty,
        "question_type": question_type,
        "native_language": "en"
    })

    # create question object based on returned data
    if question_type != "fill_blank":
        db_question = Question(
            language_code=language,
            difficulty=difficulty,
            question_type=question_type,
            question_content=question_data["question"],
            answer=question_data["correct_answer"],
            explanation=question_data["explanation"]
        )
    else:
        db_question = Question(
            language_code=language,
            difficulty=difficulty,
            question_type=question_type,
            question_content=question_data["question"] + "->" + str(question_data["choices"]),
            answer=question_data["correct_answer"],
            explanation=question_data["explanation"]
        )
    
    # save to database
    session.add(db_question)
    session.commit()
    session.refresh(db_question)
    
    return db_question
    