# Use the official Python image as the base image
#FROM registry.access.redhat.com/ubi9/python-312@sha256:dad2d6acf3f5e48d26abf9dbdea2f2bab3b02c62d1d6e9e0330c8d43f0c3bfb4
#FROM registry.access.redhat.com/hi/python:3.12.13
# Set the working directory in the container
#WORKDIR /app

# Copy the requirements file to the container
#COPY requirements.txt .

# Install the required Python packages
#RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code to the container
#COPY . .

# Expose the port FastAPI will run on
#EXPOSE 8000

# Command to run the FastAPI application using uvicorn
#CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]


# Build stage
FROM registry.access.redhat.com/hi/python:3.12-builder AS builder
USER root
COPY requirements.txt .
RUN python3.12 -m venv /opt/venv \
 && /opt/venv/bin/pip install --no-cache-dir -r requirements.txt

# Runtime stage
FROM registry.access.redhat.com/hi/python:3.12.13
COPY --from=builder --chown=1001:0 /opt/venv /opt/venv
COPY --from=builder /usr/lib64/libstdc++.so.6* /usr/lib64/
ENV PATH="/opt/venv/bin:$PATH"
WORKDIR /app
COPY --chown=1001:0 . .
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]