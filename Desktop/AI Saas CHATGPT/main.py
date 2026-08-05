from fastapi import FastAPI
from backend.chat import router as chat_router

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app = FastAPI()

@app.get("/")
def home():
    return {"message": "AI SaaS ChatGPT Running"}

app.include_router(chat_router)