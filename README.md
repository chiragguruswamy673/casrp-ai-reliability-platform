# CASRP – AI-Driven Reliability Platform

CASRP (Cognitive Autonomous System Reliability Platform) is an **AI-inspired reliability and QA intelligence system** that ingests real test execution results, maintains a digital twin of system state, assesses deployment risk, detects flaky tests, proposes remediation actions, and generates incident summaries.

This project is designed to demonstrate **real-world system thinking**, not just automation.

---

## 🚀 Key Capabilities

### 🧠 Intelligence
- Digital Twin of system state
- Autonomous risk assessment
- Explainable AI reasoning
- Incident narrative generation

### 🧪 QA & Testing
- Real **TestNG XML ingestion**
- Event-driven test failure handling
- **Flaky test detection across runs**
- Failure severity classification

### ⚙️ DevOps
- Fully Dockerized runtime
- Production-like execution
- Stateless container design

### 👁️ Observability
- Incident timelines
- Risk-based severity
- Memory-driven analysis

---
## 🏗️ High-Level Architecture

┌─────────────┐
│ Selenium / │
│ TestNG │
│ Test Runs │
└──────┬──────┘
│ testng-results.xml
▼
┌──────────────────────────┐
│ CASRP API (FastAPI) │
│ │
│ /ingest/testng │
│ /event/* │
│ /twin/state │
│ /observe/* │
└─────────┬────────────────┘
│
▼
┌──────────────────────────┐
│ Digital Twin │
│ - Services │
│ - DB schema │
│ - Test failures │
│ - Risk score │
└─────────┬────────────────┘
│
▼
┌──────────────────────────┐
│ AI Reasoning Layer │
│ - Risk Predictor │
│ - Healing Suggestions │
│ - Flaky Analyzer │
│ - Incident Summarizer │
└─────────┬────────────────┘
│
▼
┌──────────────────────────┐
│ Memory Layer │
│ - Event history │
│ - Failure counts │
│ - Incident timelines │
└──────────────────────────┘

## 🔄 End-to-End Flow

Test Execution
↓
TestNG XML Report
↓
/ingest/testng
↓
TEST_FAILURE events
↓
Digital Twin Update
↓
Risk Assessment
↓
Flaky Detection
↓
Healing Suggestions
↓
Incident Summary

---

## 🧪 Flaky Test Detection Logic

| Failures (same test) | Classification |
|---------------------|----------------|
| 1                   | Unstable       |
| 2                   | Flaky          |
| ≥3                  | Highly Flaky   |

This prevents false positives and mirrors real QA reliability practices.

---

## 📦 Tech Stack


API - FastAPI 
Language - Python 3.11 
Containerization - Docker 
Testing Input - Selenium / TestNG 
AI Logic - Rule-based, explainable reasoning
Storage - In-memory (design choice) 

---

## ▶️ Running the Project (Docker)

### Prerequisites
- Docker Desktop

### Run
```bash
docker compose up --build
```
Open:
```bash
http://localhost:8000/docs
```
## 🧪 Key API Endpoints
/ingest/testng	- Upload TestNG XML reports
/twin/state - View current digital twin
/twin/heal - View healing suggestions
/observe/incident -	Incident summary
/observe/flaky - Flaky test analysis

## 📊 Example Output
Flaky Detection
``` json
{
  "test_name": "testInvalidLogin",
  "failures": 3,
  "status": "highly_flaky"
}
```
Incident Summary
```json
Copy code
{
  "severity": "medium",
  "risk_score": 0.6,
  "summary": "Incident detected with medium severity due to repeated test failures."
}
```
## 🧠 Design Philosophy
Deterministic over black-box AI

Explainability over complexity

Safety before autonomy

Real signals, no hallucinations

## 🏆 Why This Project Matters
Most QA or DevOps projects stop at test execution.

CASRP goes further:

Understands test reliability

Reasons about system risk

Suggests safe remediation

Builds incident narratives

This reflects real SRE and platform engineering thinking.

## 📌 Future Enhancements (Optional)
Persistent storage

Kubernetes deployment

Authentication & RBAC

Trend analysis dashboards

## 👤 Author
Chirag Guruswamy