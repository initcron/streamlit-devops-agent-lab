import sys
import os

# Add the project root directory to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

import streamlit as st
from components.ollama_utils import check_ollama_connection, get_available_models, generate_response
from components.kube_utils import check_kubernetes_connection, get_pods, get_pod_logs, get_pod_metrics
from components.prom_utils import PrometheusClient
from config import Config
import altair as alt
import pandas as pd
from datetime import datetime, timedelta
import json

# App Constants
APP_NAME = "Agentic DevOps Lab"
APP_VERSION = "0.1"
APP_DESCRIPTION = "A Streamlit-based web interface for DevOps engineers to interact with LLMs, monitor Kubernetes clusters, and analyze system metrics."
FOOTER_MESSAGE = "This Learning App is created by [Gourav Shah](https://www.linkedin.com/in/gouravshah/). Visit [School of Devops](https://schoolofdevops.com) to start your AI/MLOps Journey."

# Initialize Prometheus client
prom_client = PrometheusClient()

# ----------------------------
# UI Configuration
# ----------------------------
st.set_page_config(
    page_title=APP_NAME,
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Add sidebar with version info
with st.sidebar:
    st.title(APP_NAME)
    st.markdown(f"### Version {APP_VERSION}")
    st.markdown("Module 0: Setup & Playground")
    st.markdown("---")
    st.markdown("### Features")
    st.markdown("""
    - 🏠 Setup Check
    - 🤖 LLM Playground
    - 📊 Observability Explorer
    """)
    st.markdown("---")
    st.markdown(FOOTER_MESSAGE)

# Main tabs
tabs = st.tabs(["🏠 Setup Check", "🤖 LLM Playground", "📊 Observability"])

# ----------------------------
# Tab 1: Setup Check
# ----------------------------
with tabs[0]:
    st.title(f"Welcome to {APP_NAME}")
    st.markdown(APP_DESCRIPTION)
    
    st.subheader("🔍 System Setup Status")
    
    # Status columns
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### Ollama Status")
        ollama_status = check_ollama_connection()
        st.metric("Service Status", "✅ Running" if ollama_status else "❌ Not Running")
        if ollama_status:
            models = get_available_models()
            st.markdown("#### Available Models")
            for model in models:
                st.code(model)
        else:
            st.error(f"Ollama is not running. Please start it with: `ollama run tinyllama`")
    
    with col2:
        st.markdown("### Kubernetes Status")
        k8s_status = check_kubernetes_connection()
        st.metric("Cluster Status", "✅ Connected" if k8s_status else "❌ Not Connected")
        if k8s_status:
            pods = get_pods()
            st.metric("Running Pods", len(pods))
            with st.expander("View Pods"):
                for pod in pods:
                    st.code(f"{pod['metadata']['name']} - {pod['status']['phase']}")
        else:
            st.error("Cannot connect to Kubernetes cluster. Check your kubeconfig.")
    
    with col3:
        st.markdown("### Prometheus Status")
        prom_status = prom_client.check_connection()
        st.metric("Service Status", "✅ Connected" if prom_status else "❌ Not Connected")
        if prom_status:
            metrics = prom_client.get_metric_names()
            st.metric("Available Metrics", len(metrics))
        else:
            st.error("Cannot connect to Prometheus. Check if it's running.")

# ----------------------------
# Tab 2: LLM Playground
# ----------------------------
with tabs[1]:
    st.title("🤖 LLM Prompt Playground")
    st.markdown("""
    Experiment with local LLMs through Ollama. Try different models and prompts to see how they respond.
    """)
    
    # Model selection
    available_models = get_available_models()
    if not available_models:
        st.warning("No models available. Please ensure Ollama is running and models are pulled.")
    else:
        col1, col2 = st.columns([1, 2])
        
        with col1:
            model = st.selectbox("Choose LLM Model", available_models)
            system_prompt = st.text_area(
                "System Prompt (optional)",
                help="Set the behavior of the assistant",
                height=100
            )
        
        with col2:
            prompt = st.text_area(
                "Enter your prompt",
                height=200,
                placeholder="Type your prompt here..."
            )
        
        if st.button("Run Prompt", type="primary"):
            with st.spinner("Sending to LLM..."):
                response = generate_response(model, prompt, system_prompt)
                if "error" in response:
                    st.error(f"Error: {response['error']}")
                else:
                    st.success("LLM responded:")
                    st.markdown(response.get("response", "[No response]"))
                    
                    with st.expander("Raw Response"):
                        st.json(response)

# ----------------------------
# Tab 3: Observability
# ----------------------------
with tabs[2]:
    st.title("📊 Observability Explorer")
    st.markdown("""
    Explore your Kubernetes cluster metrics and visualize them using Prometheus queries.
    """)
    
    # Metric selection and query builder
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Metric Explorer")
        metric_names = prom_client.get_metric_names()
        selected_metric = st.selectbox("Select Metric", metric_names)
        
        if selected_metric:
            metadata = prom_client.get_metric_metadata(selected_metric)
            if metadata:
                with st.expander("Metric Details"):
                    st.json(metadata)
    
    with col2:
        st.subheader("Query Builder")
        
        # Common Kubernetes queries
        common_queries = {
            "Custom Query": "",
            "CPU Usage by Pod": 'sum(rate(container_cpu_usage_seconds_total{container!=""}[5m])) by (pod)',
            "Memory Usage by Pod": 'sum(container_memory_usage_bytes{container!=""}) by (pod)',
            "Pod Restart Count": "sum(kube_pod_container_status_restarts_total) by (pod)",
            "Available Memory on Nodes": "node_memory_MemAvailable_bytes",
            "Node CPU Usage": 'sum(rate(node_cpu_seconds_total{mode!="idle"}[5m])) by (instance)',
            "Pod Status Count": "sum(kube_pod_status_phase) by (phase)",
            "API Server Request Duration": "histogram_quantile(0.99, sum(rate(apiserver_request_duration_seconds_bucket[5m])) by (le))",
            "Network Receive Bytes by Pod": "sum(rate(container_network_receive_bytes_total[5m])) by (pod)",
            "Filesystem Usage by Node": '(node_filesystem_size_bytes{mountpoint="/"} - node_filesystem_free_bytes{mountpoint="/"}) / node_filesystem_size_bytes{mountpoint="/"} * 100',
            "Container CPU Throttling": "sum(rate(container_cpu_cfs_throttled_seconds_total[5m])) by (container)"
        }
        
        query_type = st.selectbox("Select Query Type", list(common_queries.keys()))
        
        if query_type == "Custom Query":
            promql = st.text_input(
                "Enter PromQL Query",
                value=selected_metric if selected_metric else "up",
                help="Enter a valid PromQL query"
            )
        else:
            promql = st.text_input(
                "PromQL Query",
                value=common_queries[query_type],
                help="You can modify this query or use as is"
            )
        
        # Time range selection
        col3, col4 = st.columns(2)
        with col3:
            time_range = st.selectbox(
                "Time Range",
                ["5m", "15m", "1h", "6h", "24h"],
                index=2
            )
        with col4:
            step = st.selectbox(
                "Step",
                ["1m", "5m", "15m", "1h"],
                index=0
            )
    
    if st.button("Run Query", type="primary"):
        with st.spinner("Executing query..."):
            end_time = datetime.now()
            start_time = end_time - timedelta(hours=1)  # Default to 1 hour
            
            # Convert to Unix timestamps
            end_ts = int(end_time.timestamp())
            start_ts = int(start_time.timestamp())
            
            df = prom_client.query_range(
                promql,
                start_ts,
                end_ts,
                step
            )
            
            if isinstance(df, pd.DataFrame) and not df.empty and 'error' not in df.columns:
                st.success("Query Result:")
                
                # Create interactive chart
                chart = alt.Chart(df).mark_line().encode(
                    x=alt.X('timestamp:T', title='Time'),
                    y=alt.Y('value:Q', title='Value'),
                    tooltip=[
                        alt.Tooltip('timestamp:T', title='Time'),
                        alt.Tooltip('value:Q', title='Value')
                    ]
                ).properties(
                    width='container',
                    height=400
                ).interactive()
                
                st.altair_chart(chart, use_container_width=True)
                
                with st.expander("Raw Data"):
                    st.dataframe(df)
            else:
                if 'error' in df.columns:
                    st.error(f"Error executing query: {df['error'].iloc[0]}")
                else:
                    st.warning("No data returned for the query.") 