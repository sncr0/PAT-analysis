# Makefile

DB_IMAGE_NAME=spectroscopy-db:local
DB_CONTAINER_NAME=spectroscopy-db
ENV_FILE=./global/.env
VOLUME_NAME=spectroscopy-pgdata
DB_DOCKERFILE=./src/database/Dockerfile
DB_CONTEXT=./src/database


POSTGRES_USER := $(shell grep POSTGRES_USER $(ENV_FILE) | cut -d '=' -f2)
POSTGRES_DB := $(shell grep POSTGRES_DB $(ENV_FILE) | cut -d '=' -f2)
POSTGRES_PASSWORD := $(shell grep POSTGRES_PASSWORD $(ENV_FILE) | cut -d '=' -f2)


.PHONY: db-up db-down db-rebuild db-logs db-init db-connect db-wipe wait-for-db

db-up:
	docker build -t $(DB_IMAGE_NAME) -f $(DB_DOCKERFILE) $(DB_CONTEXT)
	docker run -d \
		--name $(DB_CONTAINER_NAME) \
		--env-file $(ENV_FILE) \
		-p 5432:5432 \
		-v $(VOLUME_NAME):/var/lib/postgresql/data \
		$(DB_IMAGE_NAME)

db-down:
	docker stop $(DB_CONTAINER_NAME) || true
	docker rm $(DB_CONTAINER_NAME) || true

db-wipe:
	docker volume rm $(VOLUME_NAME) || true

wait-for-db:
	@echo "⏳ Waiting for PostgreSQL container to become healthy..."
	@until [ "$$(docker inspect -f '{{.State.Health.Status}}' $(DB_CONTAINER_NAME))" = "healthy" ]; do \
		sleep 1; \
	done
	@echo "✅ PostgreSQL is healthy!"

db-rebuild: db-down db-wipe db-up wait-for-db db-init

db-logs:
	docker logs -f $(DB_CONTAINER_NAME)

db-connect:
	@echo "Connecting to PostgreSQL as $(POSTGRES_USER) on $(POSTGRES_DB)..."
	@PGPASSWORD=$(POSTGRES_PASSWORD) psql -h localhost -U $(POSTGRES_USER) -d $(POSTGRES_DB)

db-init:
	python -c "from src.database.database import init_db; init_db()"