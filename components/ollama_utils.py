import requests
from typing import Dict, Any, Optional
from config import Config

def check_ollama_connection() -> bool:
    """Check if Ollama service is running."""
    try:
        response = requests.get(f"{Config.OLLAMA_BASE_URL}")
        return response.status_code == 200
    except:
        return False

def get_available_models() -> list:
    """Get list of available Ollama models."""
    try:
        response = requests.get(f"{Config.OLLAMA_BASE_URL}/api/tags")
        if response.status_code == 200:
            return [model["name"] for model in response.json()["models"]]
        return []
    except:
        return []

def generate_response(model: str, prompt: str, system: Optional[str] = None) -> Dict[str, Any]:
    """Generate response from Ollama model."""
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False
    }
    if system:
        payload["system"] = system
        
    try:
        response = requests.post(f"{Config.OLLAMA_BASE_URL}/api/generate", json=payload)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": str(e)}
