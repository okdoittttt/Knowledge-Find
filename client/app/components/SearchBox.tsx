'use client';

import { useState } from 'react';
import Image from 'next/image';
import React from 'react';

// API 응답 데이터의 타입
interface SearchResult {
  word: string;
  score: number;
  filename: string;
}

export default function SearchBox() {
  const [searchTerm, setSearchTerm] = useState('');
  const [searchResults, setSearchResults] = useState<SearchResult[]>([]);
  const [isLoading, setIsLoading] = useState(false); // 로딩 상태를 관리할 새로운 상태

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setSearchTerm(e.target.value);
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      handleSearch();
    }
  };

  const handleSearch = async () => {
    // 검색어가 비어있을 경우 API 호출을 막습니다.
    if (!searchTerm.trim()) {
      return;
    }

    const API_URL = "http://127.0.0.1:8000/search";
    
    const data = {
      query: searchTerm,
      limit: 5,
    };
    
    // API 호출 시작: 로딩 상태를 true로 설정
    setIsLoading(true);

    try {
      const response = await fetch(API_URL, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      });

      if (!response.ok) {
        throw new Error(`HTTP 에러 발생 ${response.status}`);
      }

      const result = await response.json();
      console.log('API 호출 성공:', result);
      setSearchResults(result.results); // API 호출 성공 후 상태 업데이트
      // setSearchTerm(''); // 검색창 초기화
      
    } catch (error) {
      console.error('API 호출 실패:', error);
      setSearchResults([]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col items-center">
      {/* 검색창 */}
      <div className="w-[500%] relative">
        <div className="relative flex items-center">
          <Image
            src="/assets/glass.png"
            alt="Magnifying glass icon"
            width={20}
            height={20}
            className="absolute left-3"
          />
          <input
            type="text"
            value={searchTerm}
            onChange={handleInputChange}
            onKeyDown={handleKeyDown}
            placeholder="검색어를 입력하세요..."
            className="w-full pl-10 pr-10 py-2 border border-white rounded-lg bg-gray-100 text-gray-900 focus:outline-none focus:ring-1 focus:ring-gray-300"
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
      </div>

      {/* 검색 결과 */}
      <div className="mt-8 w-full max-w-2xl">
        {isLoading ? (
          <p className="text-center text-gray-500">검색 중...</p>
        ) : searchResults.length > 0 ? (
          <div>
            <h2 className="text-xl font-semibold text-gray-800 mb-4">검색 결과</h2>
            <div className="space-y-4">
              {searchResults.map((item, index) => (
                <div
                  key={index}
                  className="p-4 border border-gray-200 rounded-lg shadow-sm bg-white"
                >
                  <p className="text-gray-700 font-medium">단어: {item.word}</p>
                  <p className="text-sm text-gray-500">
                    유사도: {item.score.toFixed(4)}
                  </p>
                  <p className="text-sm text-gray-500">파일: {item.filename}
                    <a
                      href={`http://127.0.0.1:8000/download/${item.filename}`}
                      className="ml-2 text-blue-500 hover:underline"
                      download
                    >
                      (다운로드)
                    </a>

                  </p>
                </div>
              ))}
            </div>
          </div>
        ) : (
          <p className="text-center text-gray-500"></p>
        )}
      </div>
    </div>
  );

}