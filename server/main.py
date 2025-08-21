from fastapi import FastAPI, UploadFile, File
import shutil
import os
from typing import List

app = FastAPI()
UPLOAD_DIRECTORY = "./files"
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/uploadfiles/")
async def create_upload_files(files: List[UploadFile] = File(...)):
    """
    여러 개의 파일을 한 번에 업로드하여 서버에 저장합니다.
    """
    uploaded_filenames = []
    
    for file in files:
        try:
            file_path = os.path.join(UPLOAD_DIRECTORY, file.filename)
            
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            
            uploaded_filenames.append(file.filename)
            
        finally:
            file.file.close()

    return {
        "message": f"{len(uploaded_filenames)}개의 파일이 성공적으로 업로드되었습니다.",
        "filenames": uploaded_filenames
    }