# Vancouver City Guide (Google ADK + Vertex AI)

A **production-oriented, mutli-agent system** that helps users explore Vancouver by understanding their location, identifying neighbourhoods, and providing grounded local context — built using **Google Agent Development Kit (ADK)** and deployed on **Vertex AI Agent Engine**.

This project focuses on **agent behavior** (planning, tool use, memory, and safety), not just chat responses.

---

## 🌍 What the Agent Does

The Vancouver City Guide assists users by:

- Asking for and understanding their street and street number
- Identifying the neighbourhood they are currently in
- Avoiding redundant actions using session-based memory
- Providing neighbourhood descriptions and history
- Linking users to relevant Wikipedia articles
- Responding safely to inappropriate inputs

All interactions are **tool-grounded, stateful, and observable**.

---

## 🧠 Agent Architecture

This is a **multi-agent system** with clear responsibilities:

### Root Agent — *Vancouver City Guide*
- Orchestrates conversation flow
- Decides which sub-agent to invoke
- Maintains session-level state
- Enforces safety via model callbacks

### Location Lookup Agent
- Validates and normalizes address input
- Detects duplicate addresses using session state
- Calls Google Maps Geocoding only when required

### Neighbourhood Info Agent
- Retrieves neighbourhood details and history
- Uses search-grounded retrieval (Vertex AI Search)
- Returns Wikipedia links and contextual summaries

---

## 🧩 Memory & State

The agent is **stateful** and uses **persistent, session-scoped memory** backed by Vertex AI Session Service.

This enables:
- Duplicate address detection
- Natural follow-up questions
- Reduced unnecessary tool calls
- More human-like interactions within a session

---

## 🔐 Safety & Guardrails

- Profanity and unsafe inputs are intercepted using a `before_model_callback`
- Unsafe inputs are blocked **before** model invocation
- Prevents unnecessary LLM calls for disallowed content

---

## ☁️ Deployment & Observability

- Deployed on **Vertex AI Agent Engine**
- Built for cloud-scale execution
- Full tracing enabled for:
  - model calls
  - tool invocations
  - state mutations

Traces are used as the primary mechanism for debugging and validation.

---

## 🔍 Evaluation Approach

The system is evaluated through:
- Trace inspection for tool selection and ordering
- Verification of state updates across turns
- Manual scoring of:
  - tool trajectory correctness
  - response quality and relevance

This approach prioritizes **real agent behavior** over synthetic benchmarks.

---

## 🔮 Future Extensions

- **Trip planning & itineraries:** Evolve the guide into a trip-planning assistant that creates location-aware itineraries for day or weekend visits.  
- **Autonomous actions:** Enable user-approved actions such as bookings, parking reservations, and ticket purchases via third-party APIs.  
- **Event-aware recommendations:** Surface current and upcoming local events to provide timely, context-aware suggestions.  
- **Public-facing UI:** Add a lightweight web or mobile interface for broader public access.

---

## 📌 Why This Project

This project demonstrates how to move from:
> *“a conversational demo”*  
to  
> *a production-oriented, agentic system designed for real users.*

It emphasizes:
- explicit tool orchestration
- stateful reasoning
- safety-first design
- cloud-native deployment
