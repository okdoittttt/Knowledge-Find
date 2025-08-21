from fastapi import FastAPI, UploadFile, File
import shutil
import os
import psycopg2
from typing import List

from db_config import POSTGRES_DB

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


@app.on_event("startup")
async def startup_event():
    create_table()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/uploadfiles/")
async def create_upload_files(files: List[UploadFile] = File(...)):
    uploaded_filenames = []
    try:
        with psycopg2.connect(**POSTGRES_DB) as conn:
            with conn.cursor() as cursor:
                for file in files:
                    # 파일 저장
                    file_path = os.path.join(UPLOAD_DIRECTORY, file.filename)
                    with open(file_path, "wb") as buffer:
                        shutil.copyfileobj(file.file, buffer)

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
