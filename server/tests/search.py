from qdrant_client import QdrantClient
from qdrant_client.http.models import Filter, FieldCondition, MatchValue
from sentence_transformers import SentenceTransformer

# 1. Qdrant 클라이언트 및 모델 연결
client = QdrantClient(host="localhost", port=6333)
model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2')
COLLECTION_NAME = "my_word_collection4"

def search_similar_vectors(query_text: str):
    # 2. 검색할 문자열을 벡터로 변환
    query_vector = model.encode(query_text).tolist()

    # 3. Qdrant에서 유사한 벡터 검색
    search_result = client.search(
        collection_name=COLLECTION_NAME,
        query_vector=query_vector,
        limit=5,  # 가장 유사한 상위 5개 결과만 반환
        with_payload=True # 페이로드(원본 텍스트)도 함께 반환
    )

    # 4. 검색 결과 출력
    print(f"'{query_text}'에 대한 검색 결과:")
    for result in search_result:
        # payload에서 'word'와 'filename'을 함께 출력
        word = result.payload.get('word', 'N/A')
        filename = result.payload.get('filename', 'N/A')
        print(f"  - 유사도: {result.score:.4f}, 파일명: '{filename}', 텍스트: '{word}'")

# --- 검색 예제 ---
search_query = "구직활동"
search_similar_vectors(search_query)

print("\n--- 다른 검색 예제 ---")
search_query = "손옥무의 2025 구직활동"
search_similar_vectors(search_query)

print("\n--- 다른 검색 예제 ---")
search_query = "2022"
search_similar_vectors(search_query)

