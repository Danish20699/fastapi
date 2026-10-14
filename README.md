# FastAPI High-Performance Backend & Microservices

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Framework-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Pydantic v2](https://img.shields.io/badge/Pydantic-v2.5%2B-E92063?logo=pydantic&logoColor=white)](https://docs.pydantic.dev/)
[![Track](https://img.shields.io/badge/Track-MLOps%20%7C%20DevOps-orange)](#)

A production-grade hands-on repository dedicated to **FastAPI**, **Starlette ASGI**, **Pydantic v2**, and modern cloud microservices for high-concurrency systems and Machine Learning model serving.

---

## 📚 Curriculum & Lab Series Roadmap

| Lab # | Lab Document | Focus Area | Status |
| :---: | :--- | :--- | :---: |
| **76** | [Lab 76: FastAPI Architecture & Internal Engine](76-fast-api-intro.md) | ASGI Triad (Starlette + Pydantic v2 + Uvicorn), Type Validation, Swagger UI, Dependency Injection | ✅ Completed |
| **77** | `77-fastapi-hello-world.md` | First Containerized FastAPI Microservice, ASGI Server Lifecycle & Health Probes | ⏳ Next |
| **78** | `78-fastapi-pydantic-crud.md` | Advanced Relational CRUD, Database Pooling & Async Session Management | ⏳ Upcoming |

---

## 🏛️ Architecture Overview

FastAPI provides an asynchronous, strongly-typed pipeline that unifies request validation, dependency injection, and automatic OpenAPI 3.0 documentation:

```text
┌─────────────────┐           HTTP/HTTPS Request           ┌──────────────────────────────────────────────┐
│  Client Tier    │  ────────────────────────────────────► │                  Server Tier                 │
│ (Browser, Mobile│                                        │ ┌──────────────┐   ┌───────────────────────┐ │
│  Frontend, cURL)│  ◄──────────────────────────────────── │ │ Reverse Proxy│──►│ ASGI Server (Uvicorn) │ │
│                 │           HTTP/HTTPS Response          │ │ (Nginx)      │   │   ▼                   │ │
└─────────────────┘                                        │ └──────────────┘   │ Starlette Middleware  │ │
                                                           │                    │   ▼                   │ │
                                                           │                    │ FastAPI Routing & DI  │ │
                                                           │                    │   ▼                   │ │
                                                           │                    │ Pydantic v2 Validator │ │
                                                           │                    └───────────┬───────────┘ │
                                                           │                                │             │
                                                           │                                ▼             │
                                                           │                    ┌───────────────────────┐ │
                                                           │                    │ Data Persistence Tier │ │
                                                           │                    │ (PostgreSQL, Redis)   │ │
                                                           │                    └───────────────────────┘ │
                                                           └──────────────────────────────────────────────┘
```

---

## 🚀 Quick Start

### 1. Clone the Repository & Install Dependencies
```bash
git clone https://github.com/Danish20699/fastapi.git
cd fastapi
pip install -r requirements.txt
```

### 2. Launch the Application
```bash
# Run via python direct runner:
python fastapi_intro_lab.py

# Or run via Uvicorn ASGI server with live auto-reload:
uvicorn main:app --reload --port 8000
```

### 3. Explore Interactive Documentation
Open your web browser:
* **Interactive Swagger UI Sandbox**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
* **ReDoc Technical Manual**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)
* **Raw OpenAPI 3.0 Schema**: [http://127.0.0.1:8000/openapi.json](http://127.0.0.1:8000/openapi.json)

---

## 🧪 Automated Testing & Verification

Run the automated test suite covering all 21 verification tests:
```bash
python test_fastapi_lab.py
```

---

## 📡 Endpoints Summary

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | API Root & Ecosystem Discovery |
| `GET` | `/health` | Kubernetes & Cloud Health Probe |
| `GET` | `/docs` | Interactive Swagger UI Sandbox |
| `GET` | `/redoc` | Interactive ReDoc Technical Manual |
| `GET` | `/openapi.json` | Machine-Readable OpenAPI 3.0 Schema |
| `GET` | `/api/v1/expeditions` | List Expeditions (Pagination & Query Filters) |
| `GET` | `/api/v1/expeditions/{id}` | Get Single Expedition (Regex Validated) |
| `POST` | `/api/v1/expeditions` | Create Expedition (Pydantic v2 Validated, 201 Created) |
| `PUT` | `/api/v1/expeditions/{id}` | Full Resource Idempotent Update |
| `PATCH`| `/api/v1/expeditions/{id}/status`| Partial State Transition |
| `DELETE`| `/api/v1/expeditions/{id}`| Privileged Deletion (`X-API-Key` Protected, 204 No Content)|
| `GET` | `/api/v1/telemetry/gondola-stream`| Live SSE Cable Car Telemetry Stream |

---

## 👤 Author & Attribution
* **Engineer**: Danish ([@Danish20699](https://github.com/Danish20699))
* **Program**: MLOps & Cloud DevOps Engineering (APR26)
* **Module**: 13 — High-Performance Python Backend Microservices

