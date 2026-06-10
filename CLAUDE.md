# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Single-file FastAPI app (`app.py`) providing country timezone lookups via `pytz`. Deployed as container on OpenShift/Kubernetes using Red Hat UBI9 Python 3.12 base image.

## Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run dev server
uvicorn app:app --host 0.0.0.0 --port 8000 --reload

# Build container
docker build -t simple-fastapi .
docker run -p 8000:8000 simple-fastapi
```

No test suite exists.

## Architecture

- **`app.py`** — entire application. FastAPI app with two endpoints: `GET /` (country list) and `GET /localtime/{country}` (timezone lookup by ISO 3166-1 alpha-2 code).
- **Observability** — OpenTelemetry tracing (console + OTLP gRPC to `localhost:4317`) and Prometheus metrics at `/metrics` via `prometheus-fastapi-instrumentator`.
- **CI** — GitHub Actions (`.github/workflows/ci.yaml`) builds and pushes container to Quay.io on main branch pushes. No test/lint steps in CI.

## Container Image

- Base: `registry.access.redhat.com/ubi9/python-312` (pinned by digest)
- Registry: `quay.io/rh_ee_swongpai/fast-localtime-check`
- Tagged by commit SHA
