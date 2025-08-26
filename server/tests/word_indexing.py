from qdrant_client import QdrantClient
from qdrant_client.http.models import TextIndexParams, TextIndexType

qdrant_client = QdrantClient(host="localhost", port=6333)

qdrant_client.create_payload_index(
    collection_name="my_word_collection",
    field_name="word",
    field_schema=TextIndexParams(
        type=TextIndexType.TEXT
    )
)

print("Full-text index created on 'word' field for 'my_word_collection'.")