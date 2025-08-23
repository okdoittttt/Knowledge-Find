from fastapi import FastAPI, UploadFile, File
import shutil
import os
import psycopg2
from typing import List

from repository.db_config import POSTGRES_DB
from repository.qdrantProcessor import QdrantProcessor
from search_engine.searchEngine import SearchEngine
from search_engine.searchModel import SearchRequest


app = FastAPI()
UPLOAD_DIRECTORY = "./files"
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)

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
async def create_upload_files(files: List[UploadFile] = File(...)):
    uploaded_filenames = []
    qdrant_processor = QdrantProcessor()

    try:
        with psycopg2.connect(**POSTGRES_DB) as conn:
            with conn.cursor() as cursor:
                for file in files:
                    # 파일 저장
                    file_path = os.path.join(UPLOAD_DIRECTORY, file.filename)
                    with open(file_path, "wb") as buffer:
                        shutil.copyfileobj(file.file, buffer)
                    
                    # Qdrant 저장{
                    _file_name = './files/' + file.filename
                    qdrant_processor.process_document(_file_name)

                    # DB 저장
                    cursor.execute(
                        "INSERT INTO public.uploaded_files (filename) VALUES (%s);",
                        (file.filename,)
                    )
                    print(f"INSERT rowcount={cursor.rowcount}")
                    uploaded_filenames.append(file.filename)

                conn.commit()
                print(f"{len(uploaded_filenames)}개의 파일명이 DB에 성공적으로 저장되었습니다.")

                # 마지막으로 삽입된 데이터 확인 (디버깅용)
                cursor.execute("SELECT id, filename, upload_time FROM public.uploaded_files ORDER BY id DESC LIMIT 1;")
                last_row = cursor.fetchone()
                print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>최근 저장된 행:", last_row)

    except (Exception, psycopg2.DatabaseError) as error:
        print(f"데이터베이스 오류: {error}")
        return {"message": "파일 업로드 중 데이터베이스 오류가 발생했습니다."}

    return {
        "message": f"{len(uploaded_filenames)}개의 파일이 성공적으로 업로드되었습니다.",
        "filenames": uploaded_filenames
    }

# 이유는 모르겠지만 해당 객체를 search_document() 안에 선언하면 모델 에러가 발생함
# 아마 SearchEngine.search_vectors()로 선언하면 정적 메서드 취급을 하는 것 같음.
# 그렇다면 호출할 때 마다 클래스의 인스턴스를 새롭게 호출하게 됨 ???? ===>>>> 뒤로가기, Queue적용하면 문제가 생기지 않을까?
search_engine = SearchEngine()

@app.post("/search")
async def search_document(request: SearchRequest):
    '''
    Qdrant에 키워드를 검색하여 유사한 단어를 반환
    '''
    results = search_engine.search_vectors(request.query, request.limit)
    return results