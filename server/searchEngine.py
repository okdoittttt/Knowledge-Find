from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
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
        '''
        try:
            query_vector = self.model.encode(qurey_text).tolist()

            search_result = self.qdrant_client.search(
                collection_name=self.collection_name,
                query_vector=query_vector,
                limit=limit,
                with_payload=True
            )

            formatted_results = [
                {
                    "score": result.score,
                    "word": result.payload.get('word'),
                    "filename": result.payload.get('filename')
                }
                for result in search_result
            ]
            return {"results": formatted_results}
        
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Search failed: {e}")



class SearchRequest(BaseModel):
    '''
    API 요청을 의한 데이터 모델
    '''
    query: str
    limit: int = 5