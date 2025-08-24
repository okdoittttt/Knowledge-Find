// components/DragAndDrop.tsx

'use client';

import { useState } from 'react';

export default function DragAndDrop() {
  const [isDragging, setIsDragging] = useState(false);
  const [files, setFiles] = useState<File[]>([]);
  const [uploadStatus, setUploadStatus] = useState('');

  const handleDragOver = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setIsDragging(false);
  };

  const handleDrop = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setIsDragging(false);
    const droppedFiles = Array.from(e.dataTransfer.files);
    setFiles(droppedFiles);
    setUploadStatus('');
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      const selectedFiles = Array.from(e.target.files);
      setFiles(selectedFiles);
      setUploadStatus('');
    }
  };
  
const uploadFiles = async () => {
    if (files.length === 0) {
        setUploadStatus('업로드할 파일이 없습니다.');
        return;
    }

    const formData = new FormData();
    files.forEach(file => {
      formData.append('files', file); 
    });

    setUploadStatus('파일 업로드 중...');

    try {
      const response = await fetch('http://127.0.0.1:8000/uploadfiles/', {
        method: 'POST',
        body: formData,
      });

      if (response.ok) {
        const result = await response.json();
        setUploadStatus(`성공: ${result.message}`);
        console.log('업로드 성공:', result);
        setFiles([]);
      } else {
        const errorText = await response.text();
        setUploadStatus(`실패: ${errorText}`);
        console.error('업로드 실패:', response.status, errorText);
      }
    } catch (e) {
      setUploadStatus('업로드 중 네트워크 오류가 발생했습니다.');
      console.error('네트워크 오류:', e);
    }
  };

  // 초기화 함수
  const resetFiles = () => {
    setFiles([]);
    setUploadStatus('');
  }

  return (
    <div className="flex flex-col items-center justify-center p-6 bg-gray-100 rounded-lg shadow-md">
      <div
        className={`w-full max-w-md p-8 text-center border-2 border-dashed rounded-lg cursor-pointer transition-colors duration-200 
          ${isDragging ? 'border-blue-500 bg-blue-50' : 'border-gray-400 bg-white'}`}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
      >
        <p className="text-gray-600 mb-2">
          파일을 여기에 드래그 앤 드롭하거나
        </p>
        <label htmlFor="file-upload" className="text-blue-600 underline cursor-pointer">
          파일을 선택하세요
        </label>
        <input
          id="file-upload"
          type="file"
          className="hidden"
          onChange={handleFileChange}
          multiple
        />
      </div>

      {files.length > 0 && (
        <div className="mt-4 w-full max-w-md">
          <h3 className="text-lg font-semibold text-gray-800">선택된 파일:</h3>
          <ul className="list-disc list-inside mt-2 text-gray-700">
            {files.map((file, index) => (
              <li key={index}>
                {file.name} ({(file.size / 1024).toFixed(2)} KB)
              </li>
            ))}
          </ul>
   <div className="flex justify-center space-x-4 mt-4">
            {/* 업로드 버튼 */}
            <button
              onClick={uploadFiles}
              className="px-6 py-2 text-white bg-blue-600 rounded-lg shadow-md hover:bg-blue-700 transition-colors duration-200"
            >
              업로드
            </button>
            {/* 검색 버튼 */}
            <button
              onClick={resetFiles}
              className="px-6 py-2 text-white bg-blue-600 rounded-lg shadow-md hover:bg-blue-700 transition-colors duration-200"
            >
              검색
            </button>
            {/* 초기화 버튼 */}
            <button
              onClick={resetFiles}
              className="px-6 py-2 text-gray-800 bg-gray-300 rounded-lg shadow-md hover:bg-gray-400 transition-colors duration-200"
            >
              초기화
            </button>
          </div>
        </div>
      )}

      {uploadStatus && (
        <p className="mt-4 text-sm font-medium text-gray-800">{uploadStatus}</p>
      )}
    </div>
  );
}