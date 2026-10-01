# Architecture

This repository contains a production-oriented foundation for PAREEK AI RED TEAM, an authorized AI-powered security assessment platform.

## Current status

The project includes:

- FastAPI backend scaffold
- PostgreSQL model schema
- Redis/Celery worker setup
- authorization and scope core
- discovery and security scanner interfaces
- report and attack path scaffolding
- Docker deployment configuration
- dashboard scaffold

## Design goals

- default SAFE mode
- explicit authorization and scope validation
- evidence-first findings
- deduplication and correlation
- no destructive operations
- redaction of sensitive values
- audit logs and structured output
