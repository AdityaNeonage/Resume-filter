import requests

from config import OLLAMA_BASE_URL


class OllamaError(RuntimeError):
    pass


def _request(method, path, *, timeout=120, **kwargs):
    url = f"{OLLAMA_BASE_URL}{path}"

    try:
        response = requests.request(method, url, timeout=timeout, **kwargs)
        response.raise_for_status()
    except requests.RequestException as exc:
        raise OllamaError(
            "Could not reach Ollama at "
            f"{OLLAMA_BASE_URL}. Start it with `ollama serve` and make sure the model is installed."
        ) from exc

    return response.json()


def list_models():
    data = _request("GET", "/api/tags", timeout=30)
    return [model["name"] for model in data.get("models", []) if model.get("name")]


def generate_text(prompt, *, model, temperature=0.7, max_tokens=512):
    data = _request(
        "POST",
        "/api/generate",
        json={
            "model": model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": temperature,
                "num_predict": max_tokens,
            },
        },
    )

    return (data.get("response") or "").strip()


def chat(messages, *, model, temperature=0.7, max_tokens=512):
    data = _request(
        "POST",
        "/api/chat",
        json={
            "model": model,
            "messages": messages,
            "stream": False,
            "options": {
                "temperature": temperature,
                "num_predict": max_tokens,
            },
        },
    )

    message = data.get("message", {})
    return (message.get("content") or "").strip()
