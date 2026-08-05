from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from .database import SessionLocal
from .models import Chat
from google import genai
from dotenv import load_dotenv
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(BASE_DIR, ".env"))

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env")

client = genai.Client(api_key=api_key)

router = APIRouter()


class ChatRequest(BaseModel):
    message: str


@router.post("/chat")
def chat_message(data: ChatRequest):
    db = SessionLocal()

    try:
        message = data.message.strip()

        if not message:
            raise HTTPException(
                status_code=400,
                detail="Message cannot be empty"
            )

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=message
        )

        reply = response.text if hasattr(response, "text") else "No response generated."

        chat = Chat(
            user_id=1,
            message=message,
            response=reply
        )

        db.add(chat)
        db.commit()
        db.refresh(chat)

        return {
            "message": message,
            "reply": reply
        }

    except HTTPException:
        raise

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        db.close()