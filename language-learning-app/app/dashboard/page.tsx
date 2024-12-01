'use client'

import axios from 'axios';
import { useRouter } from 'next/navigation';
import React, { useState } from 'react';

const DashboardPage = () => {
  const router = useRouter();
  const [selectedLanguage, setSelectedLanguage] = useState('');

  const handleSelectLanguage = (lang: string) => {
    if (lang === 'en') {
      setSelectedLanguage('en');
      router.push('/generate-lesson'); //send language code when multi-language function is added
    }
  };

  const handleLogout = () => {
    //delete session data 
    router.push('/logout'); 
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gradient-to-br from-blue-100 to-blue-300 text-center">
      <h1 className="text-4xl font-bold text-gray-800 mb-8">Choose a Language</h1>
      <div className="flex space-x-4">
        <button
          onClick={() => handleSelectLanguage('en')}
          className="px-8 py-4 rounded-lg bg-white text-blue-600 font-semibold hover:bg-blue-100 transition-all"
        >
          English
        </button>
        <button
          disabled
          onClick={() => handleSelectLanguage('es')}
          className="px-8 py-4 rounded-lg bg-gray-300 text-gray-600 font-semibold cursor-not-allowed"
        >
          Spanish
        </button>
        <button
          disabled
          onClick={() => handleSelectLanguage('fr')}
          className="px-8 py-4 rounded-lg bg-gray-300 text-gray-600 font-semibold cursor-not-allowed"
        >
          French
        </button>
      </div>
      {/* Disabled button for adding other languages */}
      <div className="mt-12">
        <button
          disabled
          className="rounded-lg bg-gray-300 px-6 py-3 text-gray-600 font-semibold cursor-not-allowed"
        >
          Add Language
        </button>
        <p className="text-sm text-gray-600 mt-2">Stay tuned for more language options!</p>
      </div>
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

export default DashboardPage;
