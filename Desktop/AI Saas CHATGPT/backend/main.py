from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.chat import router as chat_router
from backend.database import Base, engine
from backend import models

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "AI SaaS ChatGPT Running"}

app.include_router(chat_router)