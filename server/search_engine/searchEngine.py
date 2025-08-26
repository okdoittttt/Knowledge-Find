from fastapi import FastAPI, HTTPException
from qdrant_client import QdrantClient, models
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
    
    def search_hybrid(self, query_text: str, limit: int = 50):
        '''
        하이브리드 검색 (벡터 검색 + 키워드 검색)
        '''
        try:
            query_vector = self.model.encode(query_text).tolist()

            # 백터 검색
            vector_results = self.qdrant_client.search(
                collection_name=self.collection_name,
                query_vector=query_vector,
                limit=limit,
                with_payload=True
            )

            # 키워드 검색
            keyword_results = self.qdrant_client.scroll(
                collection_name=self.collection_name,
                scroll_filter=models.Filter(
                    must=[models.FieldCondition(
                        key="word",
                        match=models.MatchText(text=query_text)
                    )]
                ),
                limit=limit,
                with_payload=True
            )[0]
            combined_results = {}

            # 벡터 검색 결과에 대한 검색 결과
            for res in vector_results:
                combined_results[res.payload['filename']] = {
                    "score": res.score,
                    "word": res.payload.get("word"),
                    "filename": res.payload.get("filename")
                }

            # 키워드 검색 결과에 대한 검색 결과
            for res in keyword_results:
                filename = res.payload['filename']
                if filename in combined_results:
                    combined_results[filename]['score'] += 1.0  # 키워드에게는 +1점
                else:
                    combined_results[filename] = {
                        "score": 1.0,
                        "word": res.payload.get("word"),
                        "filename": filename
                    }

            final_result = sorted(combined_results.values(), key=lambda x: x['score'], reverse=True)

            return {"results": final_result[:limit]}
        
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Hybrid search failed: {e}")
