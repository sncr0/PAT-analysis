# db_gateway/Dockerfile

FROM python:3.12-slim as base

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    mosquitto \
    mosquitto-clients \
    && rm -rf /var/lib/apt/lists/*

# Install Python requirements
COPY ./db_gateway/requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the full project
COPY . .


# Make Python aware of top-level modules like db_gateway, core, etc.
ENV PYTHONPATH=/app


# Stage 2: Dev stage (dev-only dependencies and tools)
FROM base AS dev

# Install development tools if needed
# RUN apt-get install -y postgresql-client

# Default behavior: keep container alive for dev
CMD ["/bin/sh", "-c", "mosquitto -c db_gateway/config/mosquitto.conf & uvicorn db_gateway.api.main:app --host 0.0.0.0 --port 8080"]








FROM google/cloud-sdk:slim as prod

# Set working directory
WORKDIR /app

# Install PostgreSQL client and other required dependencies
RUN apt-get update -qq && apt-get install -y -qq postgresql-client curl mosquitto mosquitto-clients && rm -rf /var/lib/apt/lists/*

# Download and prepare the Cloud SQL Proxy binary
RUN curl -sSL -o /cloud_sql_proxy https://storage.googleapis.com/cloud-sql-connectors/cloud-sql-proxy/v2.10.1/cloud-sql-proxy.linux.amd64
RUN chmod +x /cloud_sql_proxy

# Install Python dependencies
COPY ./db_gateway/requirements.txt ./
RUN pip install -r requirements.txt --break-system-packages

# Copy the application files
COPY . .

# Copy and prepare the Cloud SQL Proxy setup script
COPY ./db_gateway/setup_proxy.sh /setup_proxy.sh
RUN chmod +x /setup_proxy.sh

# Authenticate with Google Cloud using the service account credentials
COPY ./config/gcp-creds.json /config/gcp-creds.json
RUN gcloud auth activate-service-account --key-file=/config/gcp-creds.json

# Accept PROJECT_ID as an argument at build time and set it for gcloud
ARG PROJECT_ID
RUN gcloud config set project $PROJECT_ID

# Default command: run the setup script and then keep the container alive
CMD ["/bin/sh", "-c", "mosquitto -c db_gateway/config/mosquitto.conf & /setup_proxy.sh & uvicorn db_gateway.api.main:app --host 0.0.0.0 --port 8080"]
