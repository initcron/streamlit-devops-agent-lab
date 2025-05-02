import os
from typing import Optional

class Config:
    """Configuration class for Agentic DevOps Lab."""
    
    # Ollama Configuration
    OLLAMA_HOST: str = os.getenv("OLLAMA_HOST", "http://localhost")
    OLLAMA_PORT: str = os.getenv("OLLAMA_PORT", "11434")
    OLLAMA_BASE_URL: str = f"{OLLAMA_HOST}:{OLLAMA_PORT}"
    
    # Prometheus Configuration
    PROMETHEUS_HOST: str = os.getenv("PROMETHEUS_HOST", "http://localhost")
    PROMETHEUS_PORT: str = os.getenv("PROMETHEUS_PORT", "30100")
    PROMETHEUS_BASE_URL: str = f"{PROMETHEUS_HOST}:{PROMETHEUS_PORT}"
    
    # Kubernetes Configuration
    KUBERNETES_NAMESPACE: str = os.getenv("KUBERNETES_NAMESPACE", "default")
    