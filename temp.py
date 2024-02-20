import io
from fastapi import FastAPI, File, UploadFile
import uvicorn
from fastapi.responses import StreamingResponse
app = FastAPI()


@app.post("/files/")
async def create_file(file: bytes = File()):
    with open('tmp', 'wb') as f:
        f.write(file)

@app.get("/files/")
async def get_file():
    file_like = open('tmp', 'rb')
    return StreamingResponse(file_like, media_type="text/javascript")

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):

    return {"filename": file.filename}

if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)