# commit-reliability-engine-v2

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/release/python-3110/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100.0+-009688.svg)](https://fastapi.tiangolo.com/)

An open-source reliability engine that detects high-risk code commits and triggers proactive multi-cloud failover (AWS, Azure, GCP) to maintain 99.999% availability.

## 🚀 Overview

`commit-reliability-engine-v2` acts as an intelligent sentinel between your CI/CD pipeline and production. By analyzing GitHub commits in real-time, it identifies high-risk code changes before they reach your servers. If a critical risk is detected, the engine automatically triggers a failover to stable cloud environments, ensuring zero-downtime.

📖 **Read the Full Article:** [How I Built a Commit-Aware Multi-Cloud Reliability Engine and What Two Patents Taught Me](https://medium.com/@kantamnenisri/how-i-built-a-commit-aware-multi-cloud-reliability-engine-and-what-two-patents-taught-me-e595dee315e4)

## 🧠 How It Works

1. **Listen**: Receives real-time push events from GitHub webhooks.
2. **Analyze**: Uses a rule-based engine to score the reliability risk (0-100) based on file paths, volume of changes, and commit semantics.
3. **Verify**: Checks the live health of AWS, Azure, and GCP resources.
4. **Act**: If the risk score exceeds **75**, it proactively shifts traffic to healthy cloud providers and logs a critical alert.

## 🏗 Architecture

```text
+----------------+      +--------------------------+      +-----------------------+
|                |      |                          |      |                       |
|  GitHub Webhook+----->+  Commit Risk Analyzer    +----->+  Multi-Cloud Orchestrator
|  (New Commit)  |      |  (FastAPI + ML Models)   |      |  (SDKs: Boto3, Azure, GCP)
|                |      |                          |      |                       |
+----------------+      +------------+-------------+      +-----------+-----------+
                                     |                                |
                                     v                                v
                        +------------+-------------+      +-----------+-----------+
                        |                          |      |                       |
                        |    Reliability Metrics   |      |   Cloud Health Probes |
                        |    (Historical Data)     |      |   (Active Monitoring) |
                        |                          |      |                       |
                        +--------------------------+      +-----------------------+
```

## 🛠 Quick Start

### Prerequisites
- Docker and Docker Compose
- Cloud Provider Credentials (AWS, Azure, GCP)

### Environment Variables
Required variables for full functionality (see `.env.example`):

| Variable | Description |
|----------|-------------|
| `AWS_ACCESS_KEY_ID` | AWS Access Key |
| `AZURE_SUBSCRIPTION_ID` | Azure Subscription ID |
| `GCP_PROJECT_ID` | GCP Project ID |
| `GOOGLE_APPLICATION_CREDENTIALS` | Path to GCP Service Account JSON |

### Running with Docker
1. **Clone & Enter:**
   ```bash
   git clone https://github.com/kantamnenisri/commit-reliability-engine-v2.git
   cd commit-reliability-engine-v2
   ```

2. **Launch:**
   ```bash
   docker-compose up --build
   ```

3. **Explore:**
   Interactive Docs: `http://localhost:8000/docs`

## 📡 Key API Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| `POST` | `/webhook/github` | Primary endpoint for GitHub events |
| `GET` | `/cloud-status` | Combined health report for AWS, Azure, GCP |
| `GET` | `/health` | Engine self-health check |

## 📜 Intellectual Property & Inspiration

This project is a technical implementation of the architectural concepts and reliability methodologies detailed in:
* **USPTO Patent Application 19/344,864**
* **USPTO Patent Application 19/325,718**

**Author:** Venkata Srinivas Kantamneni

## ⚖️ License

Distributed under the MIT License. See `LICENSE` for more information.
