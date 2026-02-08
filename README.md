# 🐙 Krkn-Insight: Result Analysis Prototype

### 📢 LFX Mentorship Submission (Spring 2026)
This repository is a Proof-of-Concept (PoC) developed specifically for the [LFX Mentorship Program](https://mentorship.lfx.linuxfoundation.org/). 

**Target Project:** Krkn-Chaos  
**Target Issue:** [[feature] Enhancing Krkn-AI Result Analysis with Interactive Visualization and Insights #74](https://github.com/krkn-chaos/krkn-ai/issues/74)

---

## ⚠️ Prototype Disclaimer
This repository is intended as a **Proof of Work (PoW)** to demonstrate the proposed architecture and visualization logic for Issue #74. 
- **Self-Contained Simulation:** All chaos experiment data, telemetry, and artifacts are generated internally via a simulation engine to demonstrate the UI/UX without requiring live cluster access or external cloud billing.
- **Zero-Cost Execution:** This app runs entirely on local resources and does not require paid API keys.

---

## 🎯 Project Objective
The goal of this prototype is to demonstrate how raw Krkn-AI experiment artifacts (JSON, CSV, YAML) can be transformed into an interactive, explorable visualization layer. By surfacing fitness scores, SLO breaches, and health checks through a web-based GUI, we reduce the manual effort required by engineers to interpret complex chaos outputs.

## 🛠️ Key Implementation Details
- **Unified Schema:** Built using Python `dataclasses` to structure the ingestion of potential Krkn artifacts.
- **SLO-Centric Monitoring:** Interactive time-series charts (via Plotly) with dynamic Service Level Objective (SLO) threshold markers.
- **Failure Correlation:** Logic to highlight telemetry spikes and link them to specific chaos scenarios (e.g., correlating `node-io-stress` with latency breaches).
- **AI-Ready Architecture:** A dedicated analysis tab designed to integrate with Large Language Models (LLMs) for automated root-cause reporting.

## 🏗️ Architecture
The dashboard follows a modular Python structure:
- **Simulation Engine:** Handles the logic for data generation and outcome weighting.
- **Visualization Layer:** Utilizes Plotly for granular analysis of performance regressions.
- **Session State:** Ensures data persistence during interactive "Chaos Simulation" runs.

## 📥 Installation & Usage

1. **Clone the repo:**
   ```bash
   git clone [https://github.com/satyam-coder07/krkn-insight-dashboard.git](https://github.com/satyam-coder07/krkn-insight-dashboard.git)
   cd krkn-insight-dashboard

2. **Install dependencies:**
    ```bash
    pip install -r requirements.txt

3. **Launch the dashboard prototype:**
    ```bash
    streamlit run app.py