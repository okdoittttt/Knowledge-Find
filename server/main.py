from fastapi import FastAPI

#app test
app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello World"}