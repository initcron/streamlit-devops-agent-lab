import subprocess
from typing import Dict, List, Any
import json

def check_kubernetes_connection() -> bool:
    """Check if Kubernetes cluster is accessible."""
    try:
        result = subprocess.run(["kubectl", "get", "nodes"], capture_output=True, text=True)
        return result.returncode == 0
    except:
        return False

def get_pods(namespace: str = "default") -> List[Dict[str, Any]]:
    """Get list of pods in specified namespace."""
    try:
        result = subprocess.run(
            ["kubectl", "get", "pods", "-n", namespace, "-o", "json"],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            data = json.loads(result.stdout)
            return data.get("items", [])
        return []
    except:
        return []

def get_pod_logs(pod_name: str, namespace: str = "default", lines: int = 100) -> str:
    """Get logs for a specific pod."""
    try:
        result = subprocess.run(
            ["kubectl", "logs", pod_name, "-n", namespace, f"--tail={lines}"],
            capture_output=True,
            text=True
        )
        return result.stdout if result.returncode == 0 else ""
    except:
        return ""

def get_pod_metrics(pod_name: str, namespace: str = "default") -> Dict[str, Any]:
    """Get resource metrics for a specific pod."""
    try:
        result = subprocess.run(
            ["kubectl", "top", "pod", pod_name, "-n", namespace],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            lines = result.stdout.strip().split('\n')
            if len(lines) > 1:
                headers = lines[0].split()
                values = lines[1].split()
                return dict(zip(headers, values))
        return {}
    except:
        return {}
