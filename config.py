from dotenv import load_dotenv
import os

load_dotenv()

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434").rstrip("/")
DEFAULT_CHAT_MODEL = os.getenv("OLLAMA_CHAT_MODEL", "llama3.2:latest")
DEFAULT_RESUME_MODEL = os.getenv("OLLAMA_RESUME_MODEL", DEFAULT_CHAT_MODEL)
