# PAREEK AI RED TEAM

<p align="center">
  <img src="https://raw.githubusercontent.com/ethicalpareek-sys/pareek-ai-red-team/main/.github/assets/penguin-banner.png" alt="PAREEK AI RED TEAM" width="900" />
</p>

<p align="center">
  <b>Autonomous AI-Powered Web Application Security & Vulnerability Assessment Platform</b>
</p>

<p align="center">
  <img alt="Python" src="https://img.shields.io/badge/Python-3.12+-3776AB?logo=python&logoColor=white" />
  <img alt="FastAPI" src="https://img.shields.io/badge/FastAPI-0.115+-009688?logo=fastapi&logoColor=white" />
  <img alt="React" src="https://img.shields.io/badge/React-Next.js-20232A?logo=react&logoColor=61DAFB" />
  <img alt="Docker" src="https://img.shields.io/badge/Docker-Ready-2496ED?logo=docker&logoColor=white" />
  <img alt="Termux" src="https://img.shields.io/badge/Termux-Compatible-33A532?logo=android&logoColor=white" />
  <img alt="License" src="https://img.shields.io/badge/License-Apache%202.0-blue.svg" />
</p>

<p align="center">
  <strong>Authorized security research only.</strong>
</p>

---

## Overview

PAREEK AI RED TEAM is a professional, AI-assisted vulnerability assessment platform designed for:

- systems you own
- explicitly authorized penetration tests
- bug bounty programs with written permission
- lab and CTF environments
- local research environments

It combines:

- AI-assisted security analysis
- web and API discovery
- safe validation workflows
- attack-surface reasoning
- evidence-backed findings
- contextual risk prioritization
- professional reporting

This platform is not designed for unauthorized scans or hostile exploitation against third-party or unknown systems.

---

## Safety First

The platform enforces strict controls before any active testing begins:

- authorization gate
- target allowlist
- excluded targets
- request budget
- rate limiting
- time limiting
- safe mode by default
- full audit logging

The scanner refuses targets outside the configured scope and prevents scope bypass via:

- redirects
- DNS aliases
- subdomains
- parameters
- alternate ports
- IP representations
- encoded hostnames
- SSRF-like redirect chains

---

## 3D Cyber Security Vision

PAREEK AI RED TEAM is built around a serious security workflow, not a toy scanner.

It aims to deliver:

- real target modeling
- asset inventory and mapping
- authenticated and unauthenticated checks where allowed
- evidence-backed vulnerability assessment
- false-positive reduction
- attack-path analysis
- actionable remediation guidance

The project is designed to feel like a real professional security platform, while remaining safe and scope-controlled.

---

## Core Features

- AI security orchestrator
- authorized discovery engine
- browser-aware crawler
- HTTP security analysis
- API security analysis
- authz and business logic heuristics
- client-side JS and dependency checks
- upload security analysis
- exposure and configuration review
- CVE correlation and tech risk intelligence
- deduplication and correlation engine
- attack-path reasoning
- dashboard and reporting

---

## Supported Environments

### Linux / Server

Recommended for full-stack production deployment:

- Ubuntu / Debian
- Docker + Docker Compose
- PostgreSQL
- Redis
- FastAPI backend
- React/Next.js dashboard

### Termux / Android

This project is also designed with Termux usage in mind for lightweight, mobile-friendly security research scenarios.

Termux is useful for:

- local scripting and automation
- lightweight reconnaissance tooling
- Python-based analysis workflows
- experimenting in authorized lab environments

Important note:

- Docker is not always available or stable in Termux
- The recommended Termux setup is the Python backend and local tooling without container orchestration
- For full enterprise-grade scanning, a Linux VM, VPS, or cloud-hosted environment is recommended

---

## Termux Quick Start

> Works best in a user-owned lab or authorized local environment.

Install prerequisites:

```bash
pkg update && pkg upgrade
pkg install -y git python clang make libffi openssl openssl-tool redis postgresql
```

Create a virtual environment:

```bash
python -m venv .venv
. .venv/bin/activate
```

Install backend dependencies:

```bash
cd backend
pip install -r requirements.txt
cp .env.example .env
```

Start Redis locally if needed:

```bash
redis-server --daemonize yes
```

Run the API locally:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Check the service:

```bash
curl http://localhost:8000/health
```

For Termux, use a local or authorized lab target only. Do not scan arbitrary internet targets.

---

## Standard Quick Start

### 1. Configure environment

```bash
cd backend
cp .env.example .env
```

### 2. Start services

```bash
docker compose up --build
```

### 3. Run database setup

```bash
docker compose exec api python -m alembic upgrade head
```

### 4. Health check

```bash
curl http://localhost:8000/health
```

---

## Project Structure

```text
pareek-ai-red-team/
├─ backend/
│  ├─ app/
│  │  ├─ api/
│  │  ├─ core/
│  │  ├─ db/
│  │  ├─ models/
│  │  ├─ scanners/
│  │  ├─ orchestration/
│  │  ├─ services/
│  │  ├─ utils/
│  │  ├─ workers/
│  │  ├─ main.py
│  │  └─ __init__.py
│  ├─ tests/
│  ├─ requirements.txt
│  ├─ pyproject.toml
│  ├─ .env.example
│  ├─ Dockerfile
│  └─ README.md
├─ frontend/
├─ docs/
├─ docker-compose.yml
├─ README.md
├─ LICENSE
└─ .gitignore
```

---

## Architecture

- Backend: FastAPI + Pydantic + SQLAlchemy + Celery
- Database: PostgreSQL
- Queue: Redis
- Frontend: Next.js / React
- Containers: Docker
- Deployment: local or hosted environment

---

## Security Principles

- default mode is SAFE
- no scan outside allowlisted scope
- no destructive actions
- no secret exposure in reports
- every finding requires evidence
- every result should be traceable to observations
- all active actions require explicit authorization

---

## License

Apache License 2.0

---

## Important

This project is intended for:

- authorized penetration testing
- permitted bug-bounty work
- local lab testing
- CTF environments
- security research in explicitly permitted contexts

It is not intended for unauthorized testing or hostile activity against third-party systems.

---

## Notes for Maintainers

If you want to make this project even more visually rich, you can add:

- a custom 3D-style logo in `assets/`
- a project banner in the repo root
- animated dashboard branding
- Android/Termux-specific deployment notes

---

## Summary

PAREEK AI RED TEAM is a serious, evidence-oriented security platform built for safe and authorized assessment workflows. It is ready for extension into a full security pipeline with discovery, correlation, risk analysis, and reporting.

Use it responsibly, stay within scope, and keep security testing authorized.
