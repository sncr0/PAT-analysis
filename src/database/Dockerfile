# database/Dockerfile

FROM postgres:17

# Declare persistent data volume
VOLUME ["/var/lib/postgresql/data"]

# Expose default PostgreSQL port
EXPOSE 5432

HEALTHCHECK --interval=5s --timeout=3s --start-period=5s --retries=10 \
  CMD pg_isready -U $$POSTGRES_USER -d $$POSTGRES_DB || exit 1