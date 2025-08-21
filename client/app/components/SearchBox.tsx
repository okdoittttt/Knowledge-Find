'use client';

import { useState } from 'react';
import Image from 'next/image';

export default function SearchBox() {
  const [searchTerm, setSearchTerm] = useState('');

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setSearchTerm(e.target.value);
  };

  const handleSearch = () => {
    console.log(searchTerm);
  };

  return (
    <div className="w-full max-w-2xl relative">
      <input
        type="text"
        value={searchTerm}
        onChange={handleInputChange}
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