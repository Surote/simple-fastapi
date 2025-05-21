# simple-fastapi

## Purpose
This application is a simple FastAPI-based web service that provides the following functionality:

1. Displays a list of countries with their full names and ISO country codes.
2. Allows users to retrieve the current local time for a specific country using its ISO country code.
3. Serves as an example of building and deploying a FastAPI application with Docker.

## Features
- **Country List**: Returns a dictionary of countries in the format `{'TH': 'Thailand', 'US': 'United States', ...}`.
- **Local Time API**: Fetches the current local time for a given country code.
- **Dockerized Deployment**: Easily deployable using Docker.

## Endpoints
- `/`: Displays a welcome message, instructions, and a list of available countries.
- `/localtime/{country}`: Returns the local time for the specified country code.

## How to Run
1. Build and run the application using Docker:
   ```bash
   docker build -t simple-fastapi .
   docker run -p 8000:8000 simple-fastapi