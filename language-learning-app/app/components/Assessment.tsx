'use client';

import React from 'react';
import { useState } from 'react';

interface Question {
  id: number;
  type: 'mcq' | 'fill';
  question: string;
  options?: string[];
  answer: string;
}

const questions: Question[] = [
  { id: 1, type: 'mcq', question: 'What is the capital of France?', options: ['Paris', 'Rome', 'Berlin', 'Madrid'], answer: 'Paris' },
  { id: 2, type: 'fill', question: '_____ is the capital of Japan.', answer: 'Tokyo' },
  // Add more questions here
];

const Assessment: React.FC = () => {
  const [currentQuestion, setCurrentQuestion] = useState<number>(0);
  const [userAnswers, setUserAnswers] = useState<{ [key: number]: string }>({});

  const handleAnswer = (answer: string) => {
    setUserAnswers({ ...userAnswers, [currentQuestion]: answer });
  };

  const nextQuestion = () => {
    setCurrentQuestion((prev) => Math.min(prev + 1, questions.length - 1));
  };

  const prevQuestion = () => {
    setCurrentQuestion((prev) => Math.max(prev - 1, 0));
  };

  return (
    <div>
      <h2>Assessment</h2>
      <p>Question {currentQuestion + 1} of {questions.length}</p>
      <div>
        <Question question={questions[currentQuestion]} handleAnswer={handleAnswer} />
      </div>
      <div>
        <button onClick={prevQuestion} disabled={currentQuestion === 0}>Previous</button>
        <button onClick={nextQuestion} disabled={currentQuestion === questions.length - 1}>Next</button>
      </div>
    </div>
  );
};

interface QuestionProps {
  question: Question;
  handleAnswer: (answer: string) => void;
}

const Question: React.FC<QuestionProps> = ({ question, handleAnswer }) => {
  const [answer, setAnswer] = useState<string>('');

  if (question.type === 'mcq') {
    return (
      <div>
        <p>{question.question}</p>
        {question.options?.map((option) => (
          <button key={option} onClick={() => handleAnswer(option)}>
            {option}
          </button>
        ))}
      </div>
    );
  } else if (question.type === 'fill') {
    return (
      <div>
        <p>{question.question}</p>
        <input
          type="text"
          value={answer}
          onChange={(e) => setAnswer(e.target.value)}
          onBlur={() => handleAnswer(answer)}
        />
      </div>
    );
  }
  return null;
};

export default Assessment;
