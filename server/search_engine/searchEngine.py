from fastapi import FastAPI, HTTPException
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer
import os

class SearchEngine:
    def __init__(self, qdrant_host: str = "localhost", qdrant_port: int = 6333):
        '''
        SearchEngine 초기화
        Qdrant, 임베딩 로드
        '''
        self.qdrant_client = QdrantClient(host=qdrant_host, port=qdrant_port)
        self.model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2')
        self.collection_name = "my_word_collection"
    
    def search_vectors(self, qurey_text: str, limit: int = 5):
        '''
        검색 쿼리를 받은 후 Qdrant에서 유사한 벡터를 검색
        중복된 파일은 유사도가 높은 하나만 반환
        '''
        try:
            query_vector = self.model.encode(qurey_text).tolist()

            search_result = self.qdrant_client.search(
                collection_name=self.collection_name,
                query_vector=query_vector,
                limit=limit,
                with_payload=True
            )

            filtered_results = [
                {
                    "score": result.score,
                    "word": result.payload.get('word'),
                    "filename": result.payload.get('filename')
                }
                for result in search_result if result.score >= 0.4
            ]

            # 유사도가 가장 높은 하나의 파일만 반환
            unique_result = {}
            for result in filtered_results:
                filename = result['filename']
                if filename not in unique_result or result['score'] > unique_result[filename]['score']:
                    unique_result[filename] = result
            
            final_result = list(unique_result.values())
            
            return {"results": final_result}
        
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Search failed: {e}")

