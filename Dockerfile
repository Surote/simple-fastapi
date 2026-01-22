# Build stage - install dependencies
FROM registry.access.redhat.com/ubi9/python-312@sha256:e151f5a3319d75dec2a7d57241ba7bb75f1b09bc3f7092d7615ea9c5aedb114c AS builder

WORKDIR /app

# Create virtual environment and install dependencies
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


# Final stage - minimal runtime image
FROM registry.access.redhat.com/ubi9/python-312@sha256:e151f5a3319d75dec2a7d57241ba7bb75f1b09bc3f7092d7615ea9c5aedb114c

WORKDIR /app

# Copy virtual environment from builder
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy only the application code
COPY app.py .

# Expose the port FastAPI will run on
EXPOSE 8000

# Command to run the FastAPI application using uvicorn
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
