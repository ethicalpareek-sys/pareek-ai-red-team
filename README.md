# PAREEK AI RED TEAM

Autonomous AI-Powered Web Application Security & Vulnerability Assessment Platform.

A safe, evidence-first security assessment platform for authorized testing, bug-bounty research, lab environments, and authorized red-team workflows.

## Overview

PAREEK AI RED TEAM combines:

- safe discovery and scope enforcement
- HTTP, DNS, TLS, and API analysis
- vulnerability correlation and evidence tracking
- risk scoring and attack-path reasoning
- professional report generation
- developer-friendly modular architecture

The platform is designed for authorized security research only and enforces explicit scope validation before any active testing.

## Features

- authorization gate and allowlist enforcement
- asset and endpoint tracking
- scan lifecycle support for SAFE, STANDARD, DEEP, API, and AUTHENTICATED modes
- security findings with evidence and redaction
- correlation engine + attack-path analysis
- report export support
- Celery-based async workers
- FastAPI backend + PostgreSQL + Redis
- Dockerized local deployment

## Quick start

### 1. Configure environment

Copy the example environment file and adjust values:

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

If Alembic is not configured yet, use the SQL seed in `backend/app/db/migrations/init.sql`.

### 4. Health check

```bash
curl http://localhost:8000/health
```

## Architecture

- Backend: FastAPI + Pydantic + SQLAlchemy + Celery
- Database: PostgreSQL
- Queue: Redis
- Dashboard: Next.js (scaffolded)
- Containerization: Docker

## Security principles

- default mode is SAFE
- no scan outside allowlisted scope
- no destructive operations
- no secret exposure in reports
- every finding must include evidence
- every result must be traceable to real observations

## License

Apache 2.0
