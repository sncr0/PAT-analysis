#!/bin/sh

echo "📦 DB Gateway container booting in MODE=$MODE"

if [ "$MODE" = "prod" ]; then
  echo "🔐 Setting up Cloud SQL Proxy..."

  # Download Cloud SQL Proxy (only in prod)
  curl -o /cloud_sql_proxy https://dl.google.com/cloudsql/cloud-sql-proxy.linux.amd64 && \
    chmod +x /cloud_sql_proxy

  echo "🔌 Starting Cloud SQL Proxy for $CLOUD_SQL_INSTANCE..."
  /cloud_sql_proxy \
    -dir=/cloudsql \
    -instances=$CLOUD_SQL_INSTANCE=tcp:5432 \
    -credential_file=$GOOGLE_APPLICATION_CREDENTIALS &

  echo "⏳ Waiting for Cloud SQL Proxy to be ready..."
  sleep 3
fi

# Keep container alive
echo "✅ Ready for commands (MQTT, DB init, etc.)"
tail -f /dev/null
