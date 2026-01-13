# Deployment Guide — Vertex AI Agent Engine (ADK)

This document describes how to deploy the **Vancouver City Guide (ADK V2)** to **Vertex AI Agent Engine**, as well as, verify a successful deployment.

The deployment uses **Google Agent Development Kit (ADK)** and **Vertex AI Agent Engine** with tracing enabled.

## Prerequisites

### 1. Local Environment
- Python 3.10 or newer
- `gcloud` CLI installed
- Access to a Google Cloud project with billing enabled

### 2. Enable Required APIs

```bash
gcloud services enable aiplatform.googleapis.com
```
### 3. Authentication

```bash
gcloud auth application-default login
gcloud auth login
gcloud auth application-default set-quota-project <Project ID>
```
You can verify authenctication, if the following prints a long token
```bash
gcloud auth application-default print-access-token
```

### 4. Directory Structure
Ensure to maintain the provided structure for ADK to perform correctly

```text
vancouver-city-guide-adk/
├── requirements.txt
├── deploy.py
├── vancouver_city_guide/
    ├── __init__.py
    ├── agent.py (Root agent - Orchestrates conversation flow and delegates to sub-agents)
    ├── run_stateful.py (Local runner using session-based memory)
    ├── profanity_guard.py (before_model_callback implementation: Blocks inappropriate inputs before LLM invocation) 
    ├── sub_agents/
    │   ├── __init__.py
    │   ├── location_lookup/ (Calls Google Maps Geocoding API, detects duplicate addresses via session state)
    │   │   ├── __init__.py
    │   │   └── agent.py 
    │   └── neighbourhood_info/ (Vertex AI Search for RAG, Returns Wikipedia links and contextual summaries)
    │       ├── __init__.py
    │       └── agent.py 
    └── .env (Local environment variables)
```

### 5. Setting up Virtual Environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```
### 6. Setting Environment variables

```bash
GOOGLE_API_KEY = <GOOGLE_API_KEY>
GOOGLE_MAPS_API_KEY = <GOOGLE_MAPS_API_KEY>
```
### 7. Running the ADK Web Interface

```bash
adk web
```
### 8. Deploying the Agent on Agent Engine

```bash
python deploy.py
```
### 9. Deployment Successful
Upon successful deployment, the CLI should show the following

```text
Deployment successful! Resource ID: projects/<PROJECT_NUMBER>/locations/<LOCATION_ID>/reasoningEngines/<ENGINE_ID>
```
