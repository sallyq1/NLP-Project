'use client'

import axios from 'axios';
import { useRouter } from 'next/navigation';
import React from 'react'

const DashboardPage = () => {
    const router = useRouter()

    const handleGenerateLesson = async () => {

        try {
          const lang = 'en'
          const difficulty = 'easy'

          const response = await axios.post(
            `http://localhost:8000/lessons/generate?language=${lang}&difficulty=${difficulty}`
          )

          const questions = encodeURIComponent(JSON.stringify(response.data.lesson_questions));
          router.push(`/lesson?questions=${questions}`)
        }
        catch (error) {
          console.error('Error generating lesson:', error);
        }
    }
    
  return (
    <div>
      DashboardPage
      <button onClick={handleGenerateLesson} className='rounded-lg bg-white p-4 text-black'>generate new lesson</button>
    </div>
    
  )
}

export default DashboardPage

