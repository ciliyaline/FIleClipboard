import uvicorn
from fastapi import FastAPI
from routers.user import router as user_router

app = FastAPI(
    title="File Clipboard API",
)

app.include_router(user_router, prefix="/user")

if __name__ == "__main__":
    uvicorn.run(app)