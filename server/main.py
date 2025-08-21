from fastapi import FastAPI, UploadFile, File
import shutil
import os

app = FastAPI()

UPLOAD_DIRECTORY = "./files"
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    """
    file: 입략받을 파일
    처음에는 단수로 받아 테스트 한 후, 추후에 복수로 변경해야함.
    변수명도 복수형으로 변경할 것.
    """
    try:
        file_path = os.path.join(UPLOAD_DIRECTORY, file.filename)
        
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
    finally:
        file.file.close()

    return {"filename": file.filename, "message": "파일이 성공적으로 업로드되었습니다."}