'use client'

import axios from 'axios';
import { useRouter } from 'next/navigation';
import React from 'react';

const GenerateLessonPage = () => {
  const router = useRouter();

  const handleGenerateLesson = async () => {
    try {
      const lang = 'en';
      const difficulty = 'easy';

      const response = await axios.post(
        `http://localhost:8000/lessons/generate?language=${lang}&difficulty=${difficulty}`
      );

      const questions = encodeURIComponent(JSON.stringify(response.data.lesson_questions));
      router.push(`/lesson?questions=${questions}`);
    } catch (error) {
      console.error('Error generating lesson:', error);
    }
  };

  const handleLogout = () => {
    router.push('/logout'); 
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gradient-to-br from-green-100 to-green-300 text-center">
      <h1 className="text-4xl font-bold text-gray-800 mb-8">Generate a New Lesson</h1>
      <button
        onClick={handleGenerateLesson}
        className="rounded-lg bg-white px-6 py-3 text-green-600 font-semibold hover:bg-green-100 transition-all"
      >
        Generate New Lesson
      </button>

      {/* Logout Button */}
      <button
        onClick={handleLogout}
        className="mt-8 px-6 py-3 rounded-lg bg-red-600 text-white font-semibold hover:bg-red-700 transition-all"
      >
        Logout
      </button>
    </div>
  );
};

export default GenerateLessonPage;
