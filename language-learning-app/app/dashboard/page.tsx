'use client'

import axios from 'axios';
import { useRouter } from 'next/navigation';
import React, { useState } from 'react';
import Header from '../components/Header';

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
    <div className="flex flex-col items-center justify-between min-h-screen bg-gradient-to-b from-[#23AAA7]/20 to-white text-center">
      <Header/>

      <div className='-mt-[100px]'>
      <h1 className="text-4xl font-bold text-gray-800 mb-8">Choose a Language</h1>
      <div className="flex space-x-4">
        <button
          onClick={() => handleSelectLanguage('en')}
          className="px-8 py-4 rounded-lg bg-white text-[#23AAA7] font-semibold hover:bg-[#23AAA7]/10 transition-all"
        >
          English
        </button>
        <button
          disabled
          onClick={() => handleSelectLanguage('es')}
          className="px-8 py-4 rounded-lg bg-[#23AAA7]/20 text-[#23AAA7] font-semibold cursor-not-allowed"
        >
          Spanish
        </button>
        <button
          disabled
          onClick={() => handleSelectLanguage('fr')}
          className="px-8 py-4 rounded-lg bg-[#23AAA7]/20 text-[#23AAA7] font-semibold cursor-not-allowed"
        >
          French
        </button>
      </div>
      {/* Disabled button for adding other languages */}
      <div className="mt-12">
        <button
          disabled
          className="rounded-lg bg-[#23AAA7]/20 px-6 py-3 text-[#23AAA7] font-semibold cursor-not-allowed"
        >
          Add Language
        </button>
        <p className="text-sm text-gray-600 mt-2">Stay tuned for more language options!</p>
      </div>
      </div>
    </div>
  );
};

export default DashboardPage;
