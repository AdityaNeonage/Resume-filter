from config import API_KEY
from google import genai

client = genai.Client(api_key=API_KEY)

response = client.models.generate_content(
    model="gemini-3.5-flash",
    contents="Write a short story about a robot learning to love.",
)

print(response.text)
client.close()
