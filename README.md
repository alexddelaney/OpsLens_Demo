# OpsLens 🚀

OpsLens is a real-time system monitoring and anomaly detection dashboard built with FastAPI, PostgreSQL, and React.

It continuously collects machine telemetry (CPU, memory), stores time-series data, detects anomalies, and visualizes system health through a live dashboard.

---

## 🔥 Features

- Real-time CPU & memory monitoring
- Background metric collection (every 5 seconds)
- PostgreSQL time-series storage
- Automatic anomaly detection engine
- Live React dashboard with charts
- Alert severity classification (warning / critical)
- Auto-refresh frontend

---

## 🏗️ Architectur
psutil → FastAPI collector → PostgreSQL → Analytics engine → React dashd

**Backend**

- FastAPI
- SQLAlchemy
- PostgreSQL
- APScheduler
- psutil

**Frontend**

- React (Vite)
- Recharts

---

## 📊 System Overview

OpsLens runs a background scheduler that:

1. Collects real system metrics
2. Stores them in PostgreSQL
3. Runs anomaly detection
4. Serves results to the React dashboard

---

## 🚀 Getting Started

### 1 Clone the repo

```bash
git clone https://github.com/YOUR_USERNAME/opslens.git
cd opslens

### 2 Backend Setup
cd backend
pythom -m venv venv
source venv/bin/activate
pip install -r requirements.txt

Start the Backend
uvicorn main:app 

Backend Runs at: 
http://127.0.0.1:8000

### 3. Frontend Setup 
New Terminal Run: 
cd frontend
npm install
npm run dev

Frontend Runs at: http://localhost:5173

OpsLens detects anomalies using:

Hard thresholds (CPU, memory)

Statistical spike detection vs recent history

Severity classification

📈 API Endpoints
Metrics

POST /metrics — ingest metric

GET /metrics — list recent metrics

POST /metrics/collect — manual collection

Alerts

GET /metrics/alerts — anomaly detection results

### Roadmap

 Docker deployment

 Multi-host monitoring agents

 WebSocket live streaming

 Authentication layer

 Kubernetes metrics support

🧑‍💻 Author

Alexander Delaney

Computer Science 29'  @ LSU

Focus: systems, fintech, and infrastructure

LinkedIn: https://www.linkedin.com/in/alex-delaney-742788314/


OpsLens demonstrates:

real-time data pipelines

backend scheduling systems

time-series storage patterns

anomaly detection logic

full-stack observability tooling

This project mirrors core patterns used in Datadog, New Relic, and Prometheus-based systems.
