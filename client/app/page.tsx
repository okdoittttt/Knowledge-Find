import DragAndDrop from './components/DragAndDrop';
import SearchBox from './components/SearchBox';

export default function HomePage() {
  return (
    <main className="flex min-h-screen flex-col items-center p-24">
      <div className="flex-grow flex flex-col items-center justify-center">
        <h1 className="text-4xl font-bold mb-8">문서 스캔</h1>
        <DragAndDrop />
      </div>
      
      <div className="w-full flex justify-center">
        <SearchBox />
      </div>

    </main>
  );
}