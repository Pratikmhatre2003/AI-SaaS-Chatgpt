from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr, Field
from backend.database import SessionLocal
from backend.models import User
from passlib.hash import bcrypt
from jose import jwt
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")

if not SECRET_KEY:
    raise ValueError("SECRET_KEY not found in .env")

ALGORITHM = "HS256"

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str

@router.post("/register")
def register(data: RegisterRequest):
    db = SessionLocal()

    try:
        existing_user = db.query(User).filter(User.email == data.email).first()

        if existing_user:
            raise HTTPException(
                status_code=400,
                detail="Email already registered"
            )

        new_user = User(
            email=data.email,
            password=bcrypt.hash(data.password)
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return {
            "message": "User registered successfully"
        }

    except HTTPException:
        raise

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

    finally:
        db.close()


@router.post("/login")
def login(data: LoginRequest):
    db = SessionLocal()

    try:
        user = db.query(User).filter(User.email == data.email).first()

        if not user:
            raise HTTPException(
                status_code=401,
                detail="Invalid email or password"
            )

        if not bcrypt.verify(data.password, user.password):
            raise HTTPException(
                status_code=401,
                detail="Invalid email or password"
            )

        token = jwt.encode(
            {
                "user_id": user.id,
                "email": user.email
            },
            SECRET_KEY,
            algorithm=ALGORITHM
        )

        return {
            "message": "Login successful",
            "access_token": token,
            "token_type": "bearer"
        }

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

    finally:
        db.close()