// app/page.tsx

import DragAndDrop from './components/DragAndDrop';

export default function HomePage() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-24">
      <h1 className="text-4xl font-bold mb-8">파일 업로드</h1>
      <DragAndDrop />
    </main>
  );
}