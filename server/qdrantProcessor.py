from unstructured.partition.auto import partition
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient, models
import re

class QdrantProcessor:
    def __init__(self, qdrant_host: str = "localhost", qdrant_port: int = 6333):
        """
        QdrantProcessor 초기화
        Qdrant, 엠베딩 로드
        """
        self.qdrant_client = QdrantClient(host=qdrant_host, port=qdrant_port)
        self.model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2')
        self.collection_name = "my_word_collection"
        
    def _preprocess_text(self, text: str) -> list[str]:
        """
        텍스트를 전처리하여 단어 리스트로 반환
        """
        cleaned_text = re.sub(r'[^가-힣a-zA-Z0-9\s]', ' ', text)
        words = cleaned_text.split()
        return [word for word in words if word]

    def process_document(self, filename: str):
        """
        지정된 파일을 처리 -> Qdrant에 데이터를 저장
        
        Args:
            filename (str): 처리할 파일의 경로, 이름
        """
        try:
            # 1. 전처리
            elements = partition(filename)
            full_text = " ".join([str(el) for el in elements])
            words = self._preprocess_text(full_text)

            if not words:
                print(f"경고: '{filename}'에서 추출할 단어가 없음!!!!!!!!!!!!!")
                return

            print(f"'{filename}'에서 {len(words)}개의 단어를 추출했습니다.")
            
            # 2. 단어 -> 임베딩 벡터
            embeddings = self.model.encode(words)
            vector_size = embeddings.shape[1]

            # 3. 컬랙션 생성 및 업데이트
            if self.qdrant_client.collection_exists(self.collection_name):
                self.qdrant_client.delete_collection(self.collection_name)
            
            self.qdrant_client.create_collection(
                collection_name=self.collection_name,
                vectors_config=models.VectorParams(
                    size=vector_size,
                    distance=models.Distance.COSINE
                )
            )
            
            # 4. 데이터 업로드
            points_to_upload = [
                models.PointStruct(
                    id=idx,
                    vector=embedding.tolist(),
                    payload={"word": words[idx], "filename": filename}
                )
                for idx, embedding in enumerate(embeddings)
            ]
            
            self.qdrant_client.upload_points(
                collection_name=self.collection_name,
                points=points_to_upload
            )
            
            print(f"'{self.collection_name}' 컬렉션에 {len(embeddings)}개의 벡터를 성공적으로 저장했습니다.")

        except FileNotFoundError:
            print(f"오류: '{filename}' 파일을 찾을 수 없습니다.")
        except Exception as e:
            print(f"처리 중 오류 발생: {e}")

# --- 클래스 사용 예제 ---
if __name__ == "__main__":
    processor = QdrantProcessor()
    
    # 예제 파일 경로
    test_file_path = "./files/testpdf.pdf"
    
    # QdrantProcessor를 사용하여 파일 처리
    processor.process_document(test_file_path)