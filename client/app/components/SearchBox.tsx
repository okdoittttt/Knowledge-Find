'use client';

import { useState } from 'react';
import Image from 'next/image';

export default function SearchBox() {
  const [searchTerm, setSearchTerm] = useState('');

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setSearchTerm(e.target.value);
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      handleSearch();
    }
  }

  const handleSearch = async () => {
    const API_URL = "http://127.0.0.1:8000/search";

    // Data class로 변경할 필요가 있음.
    const data = {
      query: searchTerm,
      limit: 5,
    }

    try {
      const response = await fetch(API_URL, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      });

      if (!response.ok) {
        throw new Error(`HTTP 에러 발생 ${response.status}`)
      }

      const result = await response.json();
      console.log('API 호출 성공', result)
    } catch (error) {
      console.error('API 호출 실패', error)
    }
    
  };

  return (
    <div className="w-full max-w-2xl relative">
      <input
        type="text"
        value={searchTerm}
        onChange={handleInputChange}
        onKeyDown={handleKeyDown}
        placeholder="검색어를 입력하세요..."
        className="w-full px-4 py-2 border border-white rounded-lg bg-gray-100 text-gray-900 focus:outline-none focus:ring-1 focus:ring-gray-300 pr-10"
      />
      <button
        onClick={handleSearch}
        className="group absolute right-2 top-1/2 -translate-y-1/2 p-2 rounded-full text-gray-600 hover:text-blue-500"
      >
        <div className="transition-all duration-200 ease-in-out group-hover:invert">
          <Image
            src="/assets/search.png"
            alt="Search icon"
            width={30}
            height={30}
          />
        </div>
      </button>
    </div>
  );
}