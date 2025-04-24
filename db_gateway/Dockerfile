# db_gateway/Dockerfile

FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python requirements
COPY ./db_gateway/requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the full project
COPY . .

# Make Python aware of top-level modules like db_gateway, core, etc.
ENV PYTHONPATH=/app

# Default behavior: keep container alive, but let Makefile trigger actual commands
CMD ["tail", "-f", "/dev/null"]
