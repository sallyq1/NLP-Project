from enum import Enum
from typing import List, Optional
from uuid import UUID, uuid4
from sqlmodel import SQLModel, Field
from pydantic import BaseModel

class Difficulty(str, Enum):
    easy = "easy"
    medium = "medium"
    hard = "hard"

class QuestionType(str, Enum):
    fill_blank = "fill_blank"
    writing_prompt = "writing_prompt"
    speaking = "speaking"
    matching = "matching"

class Mastery(str, Enum):
    amateur = "amateur"
    skilled = "skilled"
    mastered = "mastered"

class Language(str, Enum):
    en = "en"
    es = "es"



class Profile(SQLModel, table=True):
    __tablename__ = "profiles"
    
    user_id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    email: str
    name: str
    # languages_learning: List[Language]

class Question(SQLModel, table=True):
    __tablename__ = "questions"

    question_id: Optional[UUID] =  Field(default_factory=uuid4, primary_key=True)
    language_code: Language
    difficulty: Difficulty
    question_type: QuestionType
    question_content: str
    answer: str
    explanation: str

class User_Attempt(SQLModel, table=True):
    __tablename__ = "user_attempts"

    user_attempt_id: Optional[UUID] = Field(default=None, primary_key=True)
    user_id: UUID
    question_id: UUID
    is_correct: bool
    num_asked: int
    mastery: Mastery