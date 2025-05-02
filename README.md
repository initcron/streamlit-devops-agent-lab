# DevOps Agent Lab

A Streamlit-based web interface for DevOps engineers to interact with LLMs, monitor Kubernetes clusters, and analyze system metrics.

## Features

- 🏠 **Setup Check**: Monitor the status of Ollama, Kubernetes, and Prometheus services
- 🤖 **LLM Playground**: Interact with local LLMs through Ollama
- 🧠 **Agent Runner**: Run DevOps agents for RCA and analysis
- 📊 **Observability**: Explore Prometheus metrics and visualize data

## Prerequisites

### System Requirements
- Python 3.11.8 (recommended) or Python 3.11.x
- UV package manager (for Python environment management)
- Ollama running locally
- Kubernetes cluster (local or remote)
- Prometheus server
- kubectl configured

### Installing UV
```bash
# For macOS (using Homebrew)
brew install uv

# For Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# For Windows (using PowerShell)
iwr https://astral.sh/uv/install.ps1 -useb | iex
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/streamlit-devops-agent-lab.git
cd streamlit-devops-agent-lab
```

2. Create and activate a virtual environment using UV:
```bash
# Create a new virtual environment with Python 3.11.8
uv venv .venv --python 3.11.8

# Activate the virtual environment
# On macOS/Linux:
source .venv/bin/activate
# On Windows:
.venv\Scripts\activate
```

3. Install dependencies using UV:
```bash
# Install all dependencies from requirements.txt
uv pip install -r requirements.txt

# Or install dependencies directly
uv pip install streamlit ollama openai requests prometheus-api-client kubernetes matplotlib altair langchain uvicorn
```


4. Verify Python version:
```bash
python --version  # Should show Python 3.11.8
```

5. Start Ollama (if not already running):
```bash
# Pull and run the tinyllama model
ollama pull tinyllama
ollama run tinyllama
```

## Usage

1. Start the Streamlit app:
```bash
# Make sure you're in the virtual environment
streamlit run app.py
```

2. Open your browser and navigate to `http://localhost:8501`


## Project Structure

```
streamlit-devops-agent-lab/
│
├── app.py                         # Main Streamlit application
├── components/
│   ├── ollama_utils.py           # Ollama interaction utilities
│   ├── kube_utils.py             # Kubernetes interaction utilities
│   └── prom_utils.py             # Prometheus interaction utilities
├── agents/                        # Agent implementations
├── assets/                        # Static assets
├── requirements.txt               # Python dependencies
├── requirements-dev.txt           # Development dependencies
└── README.md                      # Project documentation
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

Apache 2.0 License - see LICENSE file for details
