import os
from unstructured.partition.auto import partition
from langchain.text_splitter import RecursiveCharacterTextSplitter

class DocumentProcessor:
    def __init__(self, chunk_size=1000, chunk_overlap=200):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
        )

    def process_document(self, file_path: str):
        """
        문서 파싱, 청크 반환
        """
        try:
            raw_text = partition(filename=file_path)
            full_text = "\n\n".join([str(el) for el in raw_text])
        except Exception as e:
            raise RuntimeError(f"문서 파싱 실패: {e}")


        texts = self.text_splitter.create_documents([full_text])

        return texts