from typing import Annotated
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from fastapi.concurrency import run_in_threadpool
from sqlmodel import Session, select
from database import get_session, supabase
from pydantic import BaseModel
from models import Difficulty, Language, Question, QuestionType, User_Attempt
from langchain.generate_questions import generate_question

# from models import User

SessionDep = Annotated[Session, Depends(get_session)]

router = APIRouter()

# generate a new question
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

# record a user's attempt and update accordingly
@router.post("/attempt")
async def record_user_attempt(
    user_id: str,
    question_id: UUID,
    user_answer: str,
    session: SessionDep
):
    if session.get(User_Attempt, (user_id, question_id)):
        question = session.get(Question, question_id) # get the question
        question_attempt = session.get(User_Attempt, (user_id, question_id))

        is_correct = question.answer.lower().strip() == user_answer.lower().strip()

        prev_mastery = question_attempt.mastery

        if is_correct and prev_mastery == "amateur":
            new_mastery = "skilled"
        elif is_correct and prev_mastery == "skilled":
            new_mastery = "mastered"
        elif not is_correct:
            new_mastery = prev_mastery
        
        new_count_asked = question_attempt.num_asked + 1

        question_attempt.is_correct = is_correct
        question_attempt.mastery = new_mastery
        question_attempt.num_asked = new_count_asked

        session.add(question_attempt)
        session.commit()
        session.refresh(question_attempt)
        print("updated question attempt: ", question_attempt)

    else: # first attempt at a question
        question = session.get(Question, question_id) # get the question

        if not question:
            raise HTTPException(status_code=404, detail="Question not found")
        
        is_correct = question.answer.lower().strip() == user_answer.lower().strip()

        question_attempt = User_Attempt(
            user_id=user_id,
            question_id=question_id,
            is_correct=is_correct,
            num_asked=1,
            mastery="amateur"
        )
    
        session.add(question_attempt)
        session.commit()
        session.refresh(question_attempt)
        print("added question attempt: ", question_attempt)
    
    return question_attempt

    
    
