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
# FastAPI의 Dependency Injection (Depends) 방식으로 SearchEngine을 요청 단위로 관리하는 방법으로 코드를 변경하는 것이 좋아보임.
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
    results = search_engine.search_hybrid(request.query, request.limit)
    return results


@app.get("/download/files/{filename}")
def download_file(filename: str):
    '''
    클라이언트 요청에 따른 파일을 반환
    '''
    file_path = f"files/{filename}"

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    
    return FileResponse(file_path, media_type='application/octet-stream', filename=filename)

