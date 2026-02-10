import streamlit as st
import pandas as pd
import plotly.express as px
import random
import time
from dataclasses import dataclass, field
from typing import List, Literal
from datetime import datetime, timedelta

# --- Application Configuration ---
st.set_page_config(
    page_title="Krkn-Insight",
    page_icon="🐙",
    layout="wide",
    initial_sidebar_state="expanded"
)

# UI styling for metric cards and alert components
st.markdown("""
    <style>
    .metric-card {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #ff4b4b;
    }
    .stAlert { border-radius: 8px; }
    div[data-testid="stMetricValue"] { font-size: 24px; }
    
    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

@dataclass
class ExperimentConfig:
    """Schema for Chaos Experiment configuration and metadata."""
    experiment_id: str
    target_cloud: str
    slo_latency_ms: int
    timestamp: datetime = field(default_factory=datetime.now)

@dataclass
class ScenarioResult:
    """Encapsulates the outcome of individual chaos injection scenarios."""
    name: str
    category: Literal['network', 'pod', 'node', 'service']
    outcome: Literal['passed', 'failed', 'warning']
    fitness_score: float
    details: str

    @property
    def is_failure(self) -> bool:
        return self.outcome == "failed"

@dataclass
class TelemetryData:
    """Structure for system-level telemetry metrics."""
    timestamp: datetime
    latency_ms: float
    cpu_usage_percent: float

def run_simulation() -> dict:
    """
    Simulates a Krkn-AI experiment run by generating synthetic artifacts.
    Returns a dictionary containing configuration, results, and telemetry.
    """
    target = random.choice(["aws-us-east-1", "gcp-europe-west3", "azure-central-india"])
    config = ExperimentConfig(
        experiment_id=f"krkn-exp-{random.randint(1000, 9999)}",
        target_cloud=target,
        slo_latency_ms=400
    )

    definitions = [
        ("pod-memory-hog", "pod"),
        ("node-io-stress", "node"),
        ("network-corruption", "network"),
        ("api-gateway-down", "service")
    ]
    
    results = []
    critical_failure_active = False

    for name, category in definitions:
        outcome = random.choices(["passed", "failed", "warning"], weights=[0.65, 0.25, 0.1])[0]
        
        # Fitness score calculation logic based on outcome
        score = 1.0 if outcome == "passed" else random.uniform(0.1, 0.6)
        if outcome == "warning": 
            score = random.uniform(0.7, 0.9)
        
        if outcome == "failed":
            critical_failure_active = True
            
        results.append(ScenarioResult(
            name=name, category=category, outcome=outcome,
            fitness_score=round(score, 2),
            details=f"Injection on {target} finished with status: {outcome}"
        ))

    # Generate 60 minutes of time-series telemetry
    telemetry_points = []
    now = datetime.now()
    
    for i in range(60):
        t = now - timedelta(minutes=60-i)
        lat = random.uniform(20, 50)
        cpu = random.uniform(10, 30)
        
        # Simulated chaos impact window (T+35 to T+45)
        if critical_failure_active and 35 <= i <= 45:
            if random.random() > 0.4:
                lat = random.uniform(300, 1200)
                cpu = random.uniform(80, 100)
        
        telemetry_points.append(TelemetryData(t, round(lat, 2), round(cpu, 2)))

    return {
        "config": config,
        "results": results,
        "telemetry": pd.DataFrame([vars(t) for t in telemetry_points])
    }

# Persistence layer to maintain state across Streamlit reruns
if 'simulation' not in st.session_state:
    st.session_state.simulation = run_simulation()

with st.sidebar:
    st.title("🐙 Chaos Control")
    st.info("Simulate a new experiment run to test visualization logic.")
    
    if st.button("Run New Experiment", type="primary"):
        with st.spinner("Injecting Chaos..."):
            time.sleep(0.8)
            st.session_state.simulation = run_simulation()
            st.rerun()

    st.divider()
    config = st.session_state.simulation['config']
    st.caption(f"**ID:** `{config.experiment_id}`")
    st.caption(f"**Target:** `{config.target_cloud}`")
    st.caption(f"**SLO:** `{config.slo_latency_ms}ms`")

# --- UI Rendering Engine ---
sim = st.session_state.simulation
config = sim['config']
results = sim['results']
df_telemetry = sim['telemetry']

st.title(f"Krkn-Insight: Analysis Report")
st.markdown(f"**Target:** `{config.target_cloud}` | **SLO Threshold:** `{config.slo_latency_ms}ms`")

# Executive Summary Metrics
col1, col2, col3, col4 = st.columns(4)

total_scenarios = len(results)
passed_scenarios = sum(1 for r in results if r.outcome == 'passed')
failed_scenarios = sum(1 for r in results if r.outcome == 'failed')
avg_fitness = sum(r.fitness_score for r in results) / total_scenarios

col1.metric("Total Scenarios", total_scenarios)
col2.metric("Passed", passed_scenarios)
col3.metric("Failed", failed_scenarios, delta_color="inverse")
col4.metric("Avg Fitness", f"{avg_fitness:.2f}", 
            delta="Healthy" if avg_fitness > 0.8 else "Degraded",
            delta_color="normal" if avg_fitness > 0.8 else "inverse")

tab_perf, tab_outcome, tab_ai = st.tabs(["Telemetry & SLOs", "Scenario Details", "AI Insights"])

with tab_perf:
    st.subheader("Network Latency vs. SLO")
    
    # Latency visualization with interactive threshold markers
    fig_lat = px.line(df_telemetry, x="timestamp", y="latency_ms", markers=True)
    fig_lat.add_hline(y=config.slo_latency_ms, line_dash="dash", line_color="red", 
                      annotation_text="SLO Limit", annotation_position="top right")
    fig_lat.add_hrect(y0=config.slo_latency_ms, y1=2000, line_width=0, fillcolor="red", opacity=0.1)
    st.plotly_chart(fig_lat, use_container_width=True)

    st.subheader("Resource Saturation")
    fig_cpu = px.area(df_telemetry, x="timestamp", y="cpu_usage_percent", color_discrete_sequence=["#FFA500"])
    st.plotly_chart(fig_cpu, use_container_width=True)

with tab_outcome:
    st.subheader("Scenario Breakdown")
    df_res = pd.DataFrame([vars(r) for r in results])
    
    fig_bar = px.bar(df_res, x="name", y="fitness_score", color="outcome",
                     color_discrete_map={"passed": "#2ecc71", "failed": "#e74c3c", "warning": "#f1c40f"})
    st.plotly_chart(fig_bar, use_container_width=True)
    
    st.dataframe(df_res.style.applymap(
        lambda x: 'background-color: #ffcccc' if x == 'failed' else '', subset=['outcome']
    ), use_container_width=True)

with tab_ai:
    st.subheader("🧠 Automated Root Cause Analysis (RCA)")
    
    # Heuristic-based insight generation
    max_latency = df_telemetry['latency_ms'].max()
    breached_slo = max_latency > config.slo_latency_ms
    culprit = next((r.name for r in results if r.outcome == 'failed'), None)
    
    if breached_slo or failed_scenarios > 0:
        st.error(" Critical Anomaly Detected")
        st.markdown(f"""
        **AI Summary of Experiment `{config.experiment_id}`:**
        
        1. **SLO Breach:** Telemetry indicates a latency spike of **{max_latency}ms**, exceeding threshold.
        2. **Correlation:** High correlation between breach and `{culprit if culprit else 'unknown'}` execution.
        3. **Impact:** System resilience in `{config.target_cloud}` is insufficient for high-load I/O or Network scenarios.
        """)
    else:
        st.success(" System Healthy")
        st.markdown(f"**AI Summary:** All metrics remained within operational boundaries.")