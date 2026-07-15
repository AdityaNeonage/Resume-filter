from config import DEFAULT_CHAT_MODEL
from ollama_client import generate_text

response = generate_text(
    "Write a short story about a robot learning to love.",
    model=DEFAULT_CHAT_MODEL,
)

print(response)
