from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if api_key:
    print("API Key loaded successfully.")
    print("First 6 characters:", api_key[:6] + "...")
else:
    print("API Key not found!")
    