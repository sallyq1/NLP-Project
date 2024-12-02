"use client";

import axios from "axios";
import { useRouter } from "next/navigation";
import React from "react";
import Header from "../components/Header";

const GenerateLessonPage = () => {
  const router = useRouter();

  const handleGenerateLesson = async () => {
    try {
      const lang = "en";
      const difficulty = "easy";

      const response = await axios.post(
        `http://localhost:8000/lessons/generate?language=${lang}&difficulty=${difficulty}`
      );

      const questions = encodeURIComponent(
        JSON.stringify(response.data.lesson_questions)
      );
      router.push(`/lesson?questions=${questions}`);
    } catch (error) {
      console.error("Error generating lesson:", error);
    }
  };

  return (
    <div className="flex flex-col justify-between min-h-screen bg-gradient-to-b from-[#1C7F81]/10 to-white text-center ">
      <Header />
      <div className="flex flex-col items-center justify-center gap-14">
        <h1 className="text-7xl font-bold text-gray-800 ">
          Generate a New Lesson
        </h1>
        <button
          onClick={handleGenerateLesson}
          className=" px-8 py-3 text-lg rounded-full  bg-[#23AAA7] text-white font-semibold hover:bg-[#23AAA7]/70 transition-all"
        >
          Generate
        </button>
      </div>
    </div>
  );
};

export default GenerateLessonPage;
