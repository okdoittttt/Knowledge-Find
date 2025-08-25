import shutil
import os
import psycopg2
from typing import List
from fastapi import UploadFile

from repository.db_config import POSTGRES_DB
from repository.qdrantProcessor import QdrantProcessor


UPLOAD_DIR = "./files"
os.makedirs(UPLOAD_DIR, exist_ok=True)

class FileUploader:
    def __init__(self):
        self.qdrant_processor = QdrantProcessor()


    async def create_upload_files(self, files: List[UploadFile]):
        '''
        여러 파일을 업로드하고 저장
        파일 메타데이터: PostgreSQL
        벡터 데이터: Qdrant
        '''
        uploaded_filenames = []
        try:
            with psycopg2.connect(**POSTGRES_DB) as conn:
                with conn.cursor() as cursor:
                    for file in files:
                        file_path = os.path.join(UPLOAD_DIR, file.filename)
                        with open(file_path, "wb") as buffer:
                            shutil.copyfileobj(file.file, buffer)

                            _file_name = f'./files/{file.filename}'
                            self.qdrant_processor.process_document(_file_name)

                            cursor.execute(
                                "INSERT INTO public.uploaded_files (filename) VALUES (%s);",
                                (file.filename,)
                            )
                            print(f'INSERT rowcount={cursor.rowcount}')
                            uploaded_filenames.append(file.filename)

                        conn.commit()
                        print(f"{len(uploaded_filenames)}개의 파일명이 DB에 성공적으로 저장되었습니다.")
                        
                    return {"message": f"{len(uploaded_filenames)}개의 파일이 성공적으로 업로드되었습니다.", "filenames": uploaded_filenames}
                
        
        except (Exception, psycopg2.DatabaseError) as error:
            print(f'데이터베이스 오류: {error}')
            raise Exception("파일 업로드 중 데이터베이스 오류 발생")
