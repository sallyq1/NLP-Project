'use client'
import { useSearchParams } from 'next/navigation'
import React, { useEffect, useState } from 'react'
import {QuestionCard} from './questionCard'
import { useRouter } from 'next/navigation';

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
  const [isAnswerSubmitted, setIsAnswerSubmitted] = useState(false)
  const router = useRouter();

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

  const handleLogout = () => {
    router.push('/logout')
  };

  const handleExitLesson = () => {
    router.push('/dashboard')
  }

  const handleAnswerSubmission = (submitted: boolean) => {
    setIsAnswerSubmitted(true)
  }

  const handleNextQuestion = () => {
    const allQuestions = getAllQuestions() // array of all questions

    // update index of question if there are more questions left to ask
    if (currentQuestionIndex < allQuestions.length - 1) {
      setCurrentQuestionIndex(prev => prev + 1)
      setIsAnswerSubmitted(false)
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
    <div className='flex flex-col items-center justify-center h-screen space-y-4 '>
    <div className='text-lg text-black/50 font-semibold tracking-wide'>
      QUESTION {currentQuestionIndex + 1} OF {questions.length}
    </div>
   
   <div className='shadow-xl rounded-3xl p-10'>
    <QuestionCard
      id={currentQuestion.id}
      questionType={currentQuestion.question_type}
      question={currentQuestion.question}
      onAnswerSubmit={handleAnswerSubmission} // Callback when answer is submitted
    />
</div>
   

    {/* Next Question Button */}
    <button
      onClick={handleNextQuestion}
      className={`px-8 py-3 text-lg rounded-full  bg-[#23AAA7] text-white  ${
        isAnswerSubmitted && currentQuestionIndex < questions.length - 1
          ? 'hover:bg-[#23AAA7] cursor-pointer'
          : 'bg-[#23AAA7]/50 cursor-not-allowed'
      }`}
      disabled={!isAnswerSubmitted || currentQuestionIndex >= questions.length - 1}
    >
      {currentQuestionIndex < questions.length - 1 ? 'Next Question' : 'End of Lesson'}
    </button>

    {/* Logout and Exit Buttons */}
    <div className='absolute top-4 right-4 space-x-4'>
      <button
        onClick={handleExitLesson}
        className='px-8 py-3 text-lg rounded-full  bg-[#23AAA7]/20 text-[#23AAA7] font-semibold hover:bg-[#23AAA7]/40 transition-all'
      >
        Exit Lesson
      </button>
      <button
        onClick={handleLogout}
        className='px-8 py-3 text-lg rounded-full bg-[#23AAA7]   text-white font-semibold hover:bg-[#23AAA7]/80 transition-all'
      >
        Logout
      </button>
    </div>
  </div>
)
}

export default LessonPage