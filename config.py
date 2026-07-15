from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = (
    os.getenv("GEMINI_API_KEY")
    or os.getenv("GOOGLE_API_KEY")
    or os.getenv("GEMINI_API_KEY")
)

if not API_KEY:
    raise RuntimeError("Missing API key. Set GEMINI_API_KEY in your .env file.")


