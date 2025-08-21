// components/DragAndDrop.tsx

'use client';

import { useState } from 'react';

export default function DragAndDrop() {
  const [isDragging, setIsDragging] = useState(false);
  const [files, setFiles] = useState<File[]>([]);

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
    // droppedFiles를 서버에 업로드하는 로직을 여기에 추가
    console.log(droppedFiles);
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      const selectedFiles = Array.from(e.target.files);
      setFiles(selectedFiles);
      // selectedFiles를 서버에 업로드하는 로직을 여기에 추가
      console.log(selectedFiles);
    }
  };

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
          <h3 className="text-lg font-semibold text-gray-800">업로드할 파일:</h3>
          <ul className="list-disc list-inside mt-2 text-gray-700">
            {files.map((file, index) => (
              <li key={index}>
                {file.name} ({(file.size / 1024).toFixed(2)} KB)
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}