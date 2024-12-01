import asyncio
from typing import Annotated, List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from fastapi.concurrency import run_in_threadpool
from sqlmodel import Session, select
from ..database import get_session, supabase
from pydantic import BaseModel
from ..models import Difficulty, Language, Question, QuestionType, User_Attempt
from ..langchain.generate_questions import generate_question
from ..dependencies import verify_jwt
from short_answer_eval import check_answer

# from models import User

SessionDep = Annotated[Session, Depends(get_session)]

router = APIRouter()

# generate a new question
@router.post("/generate")
async def generate_store_question(
    language: str,
    difficulty: str,
    session: SessionDep
):
     
    question_data = await run_in_threadpool(generate_question, {
        "language": language,
        "difficulty": difficulty,
        "native_language": "en"
    })

    lesson_questions = []
    for fillBlankQuestion in question_data["fill_blank_questions"]:
        db_question = Question(
            language_code=language,
            difficulty=difficulty,
            question_type="fill_blank",
            question_content=fillBlankQuestion["question"] + "->" + str(fillBlankQuestion["choices"]),
            answer=fillBlankQuestion["correct_answer"],
            explanation=fillBlankQuestion["explanation"]
        )

        lesson_questions.append(db_question)

    for writingPromptQuestion in question_data["writing_prompt_questions"]:
        db_question = Question(
            language_code=language,
            difficulty=difficulty,
            question_type="writing_prompt",
            question_content=writingPromptQuestion["question"],
        )

        lesson_questions.append(db_question)

    # Add all questions to the session and commit in one batch
    session.add_all(lesson_questions)
    session.commit()
    
    print(lesson_questions)

    return {"lesson_questions": [
        {
            "id": q.question_id,
            "question_type": q.question_type,
            "question": q.question_content,
            "explanation": q.explanation if q.explanation else ""
        } for q in lesson_questions
    ]}

# record a user's attempt and update accordingly
@router.post("/attempt")
async def record_user_attempt(
    question_id: UUID,
    user_answer: str,
    session: SessionDep,
    user_id: UUID
):
    if session.get(User_Attempt, (user_id, question_id)):
        question = session.get(Question, question_id) # get the question
        question_attempt = session.get(User_Attempt, (user_id, question_id))

        # test your functions here --> bool
        if question.question_type == "writing_prompt":
            is_correct = check_answer(question.question_content, user_answer)
        else:
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
                
        if question.question_type == "writing_prompt":
            is_correct = check_answer(question.question_content, user_answer)
        else:
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
    
    return {"is_correct": is_correct}

    
"""
TO DO:
x recorded user attempt
x generate question and store in db
x edit question generation to only generate the answer in the answer field

generate a test of 6 questions with other question types
""" 