# simple-fastapi
![ci workflow](https://github.com/Surote/simple-fastapi/actions/workflows/ci.yaml/badge.svg)

![Kubernetes](https://img.shields.io/badge/kubernetes-%23326ce5.svg?style=for-the-badge&logo=kubernetes&logoColor=white)
![Red Hat](https://img.shields.io/badge/Red%20Hat-EE0000?style=for-the-badge&logo=redhat&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)

## Purpose
This application is a simple FastAPI-based web service that provides the following functionality:

1. Displays a list of countries with their full names and ISO country codes.
2. Allows users to retrieve the current local time for a specific country using its ISO country code.
3. Serves as an example of building and deploying a FastAPI application with Docker.

## Features
- **Country List**: Returns a dictionary of countries in the format `{'TH': 'Thailand', 'US': 'United States', ...}`.
- **Local Time API**: Fetches the current local time for a given country code.

## Endpoints
- `GET /`
  - Displays a welcome message, instructions, and a list of available countries.
- `GET /localtime/{country}`
  - Returns the local time, **timezone name**, and country name for the specified ISO 3166-1 alpha-2 country code.
  - **Example Response**:
    ```json
    {
      "country": "United States",
      "timezone": "America/New_York",
      "local_time": "2023-10-27 10:30:00"
    }
    ```
- `GET /docs`
  - Interactive API documentation (Swagger UI).
- `GET /metrics`
  - Prometheus metrics endpoint.

## Local Development
1.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
2.  **Run the application**:
    ```bash
    uvicorn app:app --host 0.0.0.0 --port 8000 --reload
    ```
3.  **Test**: Open [http://localhost:8000/docs](http://localhost:8000/docs) in your browser.

## Observability
-   **OpenTelemetry**: The application is instrumented with OpenTelemetry to trace requests. Traces are exported to the console and an OTLP collector (default: `localhost:4317`).
-   **Prometheus**: Metrics are exposed at `/metrics`.

## Deployment
1. Build and run the application using Docker:
   ```bash
   docker build -t simple-fastapi .
   docker run -p 8000:8000 simple-fastapi

2. with k8s image can be found here `quay.io/rh_ee_swongpai/fast-localtime-check`