# db_gateway/Dockerfile

FROM python:3.12-slim as base

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
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
CMD ["tail", "-f", "/dev/null"]


FROM google/cloud-sdk:slim as prod

WORKDIR /app

# Install PostgreSQL client (required for production)
RUN apt-get update && apt-get install -y postgresql-client && rm -rf /var/lib/apt/lists/*

# Copy and prepare the Cloud SQL Proxy setup script
COPY ./db_gateway/setup_proxy.sh /setup_proxy.sh
RUN chmod +x /setup_proxy.sh

# Authenticate with Google Cloud
COPY ./config/gcp-creds.json /config/gcp-creds.json
RUN gcloud auth activate-service-account --key-file=/config/gcp-creds.json

ARG PROJECT_ID
# Set the default project for gcloud
RUN gcloud config set project $PROJECT_ID

# Command to run the setup script and then keep the container alive
CMD ["/bin/sh", "-c", "\
    echo '📦 Starting container in MODE=$MODE' && \
    if [ \"$MODE\" = \"prod\" ]; then \
      echo '🔐 Setting up Cloud SQL Proxy...' && \
      /setup_proxy.sh ; \
    else \
      echo '🧪 Dev mode: skipping Cloud SQL Proxy setup' ; \
    fi && \
    tail -f /dev/null"]