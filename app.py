import streamlit as st
from components.ollama_utils import check_ollama_connection, get_available_models, generate_response
from components.kube_utils import check_kubernetes_connection, get_pods, get_pod_logs, get_pod_metrics
from components.prom_utils import PrometheusClient
import altair as alt
import pandas as pd
from datetime import datetime, timedelta

# Initialize Prometheus client
prom_client = PrometheusClient()

# ----------------------------
# UI Configuration
# ----------------------------
st.set_page_config(page_title="DevOps Agent Lab", layout="wide")
tabs = st.tabs(["🏠 Setup Check", "🤖 LLM Playground", "🧠 Agent Runner", "📊 Observability"])

# ----------------------------
# Tab 1: Setup Check
# ----------------------------
with tabs[0]:
    st.title("Welcome to DevOps Agent Lab")
    st.subheader("🔍 System Setup Status")

    col1, col2, col3 = st.columns(3)
    with col1:
        ollama_status = check_ollama_connection()
        st.metric("Ollama Running", "✅" if ollama_status else "❌")
        if ollama_status:
            st.write("Available models:", ", ".join(get_available_models()))
    with col2:
        k8s_status = check_kubernetes_connection()
        st.metric("Kubernetes Ready", "✅" if k8s_status else "❌")
        if k8s_status:
            pods = get_pods()
            st.write(f"Running pods: {len(pods)}")
    with col3:
        prom_status = prom_client.check_connection()
        st.metric("Prometheus Connected", "✅" if prom_status else "❌")
        if prom_status:
            st.write("Available metrics:", len(prom_client.get_metric_names()))

# ----------------------------
# Tab 2: LLM Playground
# ----------------------------
with tabs[1]:
    st.header("🤖 LLM Prompt Playground")
    
    # Model selection
    available_models = get_available_models()
    if not available_models:
        st.warning("No models available. Please ensure Ollama is running and models are pulled.")
    else:
        model = st.selectbox("Choose LLM Model", available_models)
        
        # System prompt (optional)
        system_prompt = st.text_area("System Prompt (optional)", 
                                   help="Set the behavior of the assistant")
        
        # User prompt
        prompt = st.text_area("Enter your prompt")
        
        if st.button("Run Prompt"):
            with st.spinner("Sending to LLM..."):
                response = generate_response(model, prompt, system_prompt)
                if "error" in response:
                    st.error(f"Error: {response['error']}")
                else:
                    st.success("LLM responded:")
                    st.write(response.get("response", "[No response]"))
                    with st.expander("Raw JSON"):
                        st.json(response)

# ----------------------------
# Tab 3: Agent Runner
# ----------------------------
with tabs[2]:
    st.header("🧠 Run DevOps Agent")
    
    # Agent selection
    agent = st.selectbox("Choose Agent Type", ["LangChain RCA Agent", "BeeAI Agent"])
    
    # Pod selection
    pods = get_pods()
    pod_names = [pod["metadata"]["name"] for pod in pods]
    pod_name = st.selectbox("Select Pod", pod_names)
    
    # Time window selection
    time_window = st.selectbox("Select Time Window", ["5m", "10m", "1h", "6h", "24h"])
    
    if st.button("Run Agent"):
        with st.spinner("Running analysis..."):
            # Get pod metrics
            metrics = get_pod_metrics(pod_name)
            if metrics:
                st.subheader("Pod Metrics")
                st.json(metrics)
            
            # Get pod logs
            logs = get_pod_logs(pod_name)
            if logs:
                st.subheader("Recent Logs")
                st.text_area("Logs", logs, height=200)
            
            # Run Prometheus analysis
            end_time = datetime.now()
            start_time = end_time - timedelta(hours=1)  # Default to 1 hour
            promql = f'container_memory_usage_bytes{{pod="{pod_name}"}}'
            df = prom_client.query_range(promql, start_time.isoformat(), end_time.isoformat())
            
            if not df.empty:
                st.subheader("Memory Usage")
                chart = alt.Chart(df).mark_line().encode(
                    x='timestamp:T',
                    y='value:Q'
                ).interactive()
                st.altair_chart(chart, use_container_width=True)

# ----------------------------
# Tab 4: Observability
# ----------------------------
with tabs[3]:
    st.header("📊 Prometheus Metrics Explorer")
    
    # Metric selection
    metric_names = prom_client.get_metric_names()
    selected_metric = st.selectbox("Select Metric", metric_names)
    
    if selected_metric:
        # Show metric metadata
        metadata = prom_client.get_metric_metadata(selected_metric)
        if metadata:
            st.subheader("Metric Metadata")
            st.json(metadata)
        
        # Query builder
        st.subheader("Query Builder")
        promql = st.text_input("Enter PromQL Query", f"{selected_metric}")
        
        # Time range selection
        col1, col2 = st.columns(2)
        with col1:
            time_range = st.selectbox("Time Range", ["5m", "15m", "1h", "6h", "24h"])
        with col2:
            step = st.selectbox("Step", ["1m", "5m", "15m", "1h"])
        
        if st.button("Run Query"):
            end_time = datetime.now()
            start_time = end_time - timedelta(hours=1)  # Default to 1 hour
            df = prom_client.query_range(promql, start_time.isoformat(), end_time.isoformat(), step)
            
            if not df.empty:
                st.success("Query Result:")
                chart = alt.Chart(df).mark_line().encode(
                    x='timestamp:T',
                    y='value:Q'
                ).interactive()
                st.altair_chart(chart, use_container_width=True)
                
                with st.expander("Raw Data"):
                    st.dataframe(df)
            else:
                st.warning("No data returned for the query.")
