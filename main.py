import uvicorn
from fastapi import FastAPI,Request,Response
from fastapi.middleware.cors import CORSMiddleware
from routers.user import router as user_router
from routers.database import *

app = FastAPI(
    title="File Clipboard API",
)

app.include_router(user_router, prefix="/user")

if __name__ == "__main__":
    uvicorn.run(app)


# 中间件
@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    response = Response("Internal server error", status_code=500)
    try:
        request.state.db = SessionLocal()
        response = await call_next(request)
    finally:
        request.state.db.close()
    return response


# 控制跨域资源共享
origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
