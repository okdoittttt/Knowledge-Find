from pydantic import BaseModel

class SearchRequest(BaseModel):
    '''
    API 요청을 의한 데이터 모델
    '''
    query: str
    limit: int = 5

    