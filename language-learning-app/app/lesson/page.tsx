'use client'
import { useSearchParams } from 'next/navigation'
import React, { useEffect, useState } from 'react'
import {QuestionCard} from './questionCard'

interface LessonQuestions {
    id: string
    question_type: string
    question: string
    explanation: string
}

const LessonPage = () => {
  const searchParams = useSearchParams()
  const [questions, setQuestions] = useState<any[]>([])
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0)

  useEffect(() => {
    // parse questions from search params
    const questionsParam = searchParams.get('questions')

    if (questionsParam) {
      setQuestions(JSON.parse(questionsParam))
    }
  }, [searchParams])

  console.log(questions)

  const getAllQuestions = () => {
    return questions || []
  }

  const handleNextQuestion = () => {
    const allQuestions = getAllQuestions() // array of all questions

    // update index of question if there are more questions left to ask
    if (currentQuestionIndex < allQuestions.length - 1) {
      setCurrentQuestionIndex(prev => prev + 1)
    }
  }

  // if there are no questions show loading
  if (!questions || questions.length === 0) {
    return (
      <div className='flex items-center justify-center h-screen'>
        Loading questions...
      </div>
    )
  }

  const allQuestions = getAllQuestions()
  const currentQuestion = allQuestions[currentQuestionIndex]

  return (
    <div className='flex items-center justify-center h-screen'>
      <div className='flex flex-col items-center space-y-4'>
        <QuestionCard 
          id={currentQuestion.id}
          questionType={currentQuestion.question_type}
          question={currentQuestion.question}
        />

        <button 
          onClick={handleNextQuestion}
          className='bg-blue-500 text-white px-4 py-2 rounded'
          disabled={currentQuestionIndex >= allQuestions.length - 1}
        >
          Next Question
        </button>

        <div className='text-sm text-gray-500'>
          Question {currentQuestionIndex + 1} of {allQuestions.length}
        </div>
        
      </div>
    </div>
  )
}

export default LessonPage