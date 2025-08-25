from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os
import psycopg2
from typing import List

from repository.db_config import POSTGRES_DB
from repository.filesUploader import FileUploader
from repository.qdrantProcessor import QdrantProcessor
from search_engine.searchEngine import SearchEngine
from search_engine.searchModel import SearchRequest


app = FastAPI()
UPLOAD_DIRECTORY = "./files"
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)
# 이유는 모르겠지만 해당 객체를 search_document() 안에 선언하면 모델 에러가 발생함
# 아마 SearchEngine.search_vectors()로 선언하면 정적 메서드 취급을 하는 것 같음.
# 그렇다면 호출할 때 마다 클래스의 인스턴스를 새롭게 호출하게 됨 ???? ===>>>> 뒤로가기, Queue적용하면 문제가 생기지 않을까?
search_engine = SearchEngine()
file_handler = FileUploader()


origins = [
    "http://127.0.0.1:3000",
    "http://localhost:3000",
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], # OPTIONS 메서드 포함 모든 HTTP 메서드 허용
    allow_headers=["*"], # 모든 헤더 허용
)


def create_table():
    try:
        with psycopg2.connect(**POSTGRES_DB) as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS public.uploaded_files (
                        id SERIAL PRIMARY KEY,
                        filename VARCHAR(255) NOT NULL,
                        upload_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    );
                """)
                conn.commit()
                print("테이블이 성공적으로 생성되었거나 이미 존재합니다.")
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"PostgreSQL 테이블 생성 오류: {error}")


# reload 될 때 마다 테이블을 확인할 필요가 없으므로 임시 주석 처리.
# @app.on_event("startup")
# async def startup_event():
#     create_table()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/uploadfiles/")
async def files_upload(files: List[UploadFile] = File(...)):
    '''
    데이터베이스에 파일을 업로드
    '''
    return await file_handler.create_upload_files(files)


@app.post("/search")
async def search_document(request: SearchRequest):
    '''
    Qdrant에 키워드를 검색하여 유사한 단어를 반환
    '''
    results = search_engine.search_vectors(request.query, request.limit)
    return results


@app.post("/searchImage")
async def search(query: str):
    """
    파일을 받아 Qdrant에서 유사한 단어 및 파일을 검색합니다.
    """
    try:
        results = search_engine.search_image_vectors(query)
        return results
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"잘못된 파일 접근 혹은 문서오류: {e}")


@app.get("/download/files/{filename}")
def download_file(filename: str):
    '''
    클라이언트 요청에 따른 파일을 반환
    '''
    file_path = f"files/{filename}"

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    
    return FileResponse(file_path, media_type='application/octet-stream', filename=filename)

