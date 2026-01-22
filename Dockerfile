# Use the official Python image as the base image
FROM registry.access.redhat.com/ubi9/python-312@sha256:a0a5885769d5a8c5123d3b15d5135b254541d4da8e7bc445d95e1c90595de470

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the container
COPY requirements.txt .

# Install the required Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code to the container
COPY . .

# Expose the port FastAPI will run on
EXPOSE 8000

# Command to run the FastAPI application using uvicorn
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
