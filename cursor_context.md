To help you kick off the **Streamlit-based DevOps Agent Lab Interface project using Cursor**, here’s a complete context pack and setup checklist tailored for Cursor’s coding environment. This will let you build, iterate, and ship this app rapidly.

---

## ✅ PROJECT NAME

`streamlit-devops-agent-lab`

---

## 🎯 PROJECT OBJECTIVE

Build a modular **web-based command center** for DevOps Engineers using Streamlit, allowing interaction with:

* 🧠 Local LLMs (via Ollama)
* 🤖 AI Agent Frameworks (LangChain, BeeAI)
* 📊 Prometheus for metrics
* 📄 Loki for logs
* 🐳 Kubernetes for cluster state
* ⚙️ Triggering CI/CD, RCA, Infra workflows

---

## 🧪 MVP FEATURES (PHASE 1)

| Section                       | Features                                                                                                   |
| ----------------------------- | ---------------------------------------------------------------------------------------------------------- |
| 1. **Welcome + Setup Check**  | - Show status of Ollama, Kubernetes, Prometheus<br>- Button to auto-check setup                            |
| 2. **LLM Playground**         | - Prompt input<br>- Model selector (`tinyllama`, `mistral`, etc.)<br>- Real-time output & raw JSON         |
| 3. **DevOps Agent Runner**    | - Dropdown: BeeAI / LangChain agents<br>- Inputs: pod name, repo, time window<br>- Output: reasoning chain |
| 4. **Observability Explorer** | - `kubectl get pods` + status<br>- PromQL input & graph (Altair/matplotlib)<br>- Loki log query (optional) |

---

## 🛠 TECH STACK

| Tool                     | Purpose                                      |
| ------------------------ | -------------------------------------------- |
| **Streamlit**            | UI framework                                 |
| **Ollama**               | Local LLM hosting (e.g., `tinyllama:latest`) |
| **LangChain / BeeAI**    | Agent framework                              |
| **Prometheus + Grafana** | Metrics                                      |
| **Loki**                 | Logs                                         |
| **Kubernetes (KIND)**    | Cluster environment                          |
| **Python**               | Backend logic                                |
| **Cursor**               | Dev IDE for AI-assisted coding               |

---

## 📁 FOLDER STRUCTURE

```
streamlit-devops-agent-lab/
│
├── app.py                         # Main Streamlit app
├── agents/
│   ├── langchain_runner.py       # LangChain-based agents
│   └── beeai_runner.py           # BeeAI-based agents
├── components/
│   ├── ollama_utils.py           # LLM test/check functions
│   ├── kube_utils.py             # kubectl calls
│   ├── prom_utils.py             # PromQL querying
│   └── loki_utils.py             # Log queries (optional)
├── assets/
│   └── logo.png                  # Optional logo for branding
├── requirements.txt
└── README.md
```

---

## 📦 `requirements.txt` (Cursor-ready Python env)

```txt
streamlit
ollama
openai
requests
prometheus-api-client
kubernetes
matplotlib
altair
langchain
uvicorn
beeai-framework @ git+https://github.com/bee-ai/beeai-framework.git
```

> (We can pin versions for portability if needed.)

---

## 🔧 STARTUP SCRIPTS

### 🐳 Start Ollama

```bash
ollama run tinyllama
```

### 🚀 Run Streamlit app (inside Cursor)

```bash
streamlit run app.py
```

---

## 📚 NEXT STEP: CODE GENERATION

Would you like:

1. ✅ A full **starter template** with placeholders and working tabs?
2. 🧪 A complete **Phase 1 MVP build** for testing RCA, LLMs, Prometheus?

---

## 🌐 OPTIONAL: CURSOR CONFIG FILE

If using Cursor’s built-in templates or autocomplete engine, consider adding `.cursorconfig.json`:

```json
{
  "python.autoComplete.addBrackets": true,
  "python.formatting.provider": "black",
  "python.linting.enabled": true,
  "cursor.enablePrompts": true
}
```

---

Would you like me to now generate:

* The `app.py` skeleton with all the tabs and placeholders?
* A working demo of **LLM Playground + Agent Runner + Prometheus Query** tab?

Let me know what you want first.




✅ Your MVP code is ready!

You can now copy this code directly into your Cursor IDE. The file is called app.py, and it already contains the working tabs for:

🏠 Setup Status (Ollama, Kubernetes, Prometheus)

🤖 LLM Prompt Playground (with real-time output from Ollama)

🧠 RCA Agent Runner (simulated for now)

📊 Prometheus PromQL Query and graph view

🚀 What You Can Do Next in Cursor:
Add BeeAI or LangChain real agent logic in agents/ folder.

Create utility files like ollama_utils.py, prom_utils.py for cleaner architecture.

Refactor the UI components into modular scripts for maintainability.

Build the Loki integration and Mini Agent Builder tab (Phase 2).

Would you like me to scaffold the folder structure or utility files next?