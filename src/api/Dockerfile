# Use a lightweight Python base image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file from the repository root (build context is the repository root)
COPY requirements.txt ./

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire src directory into the container
COPY src/ ./src/

# Expose the API port
EXPOSE 8000

# Set environment variables (can be overridden by docker-compose)
ENV DATABASE_URL=postgresql://postgres:postgres@db:5432/patdb
ENV SECRET_TOKEN=secret-token

# Command to run the API server with Uvicorn
CMD ["uvicorn", "src.api.routes:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
