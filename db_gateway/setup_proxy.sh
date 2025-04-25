#!/bin/sh

echo "📦 DB Gateway container booting in MODE=$MODE"

if [ "$MODE" = "prod" ]; then
  echo "🔐 Setting up Cloud SQL Proxy..."

  # Download Cloud SQL Proxy
  curl -sSL -o /cloud_sql_proxy https://storage.googleapis.com/cloud-sql-connectors/cloud-sql-proxy/v2.10.1/cloud-sql-proxy.linux.amd64
  chmod +x /cloud_sql_proxy

  echo "🔌 Starting Cloud SQL Proxy for $CLOUD_SQL_INSTANCE..."
  rm -f .db_proxy.log .db_proxy.pid
    stdbuf -oL /cloud_sql_proxy \
      -dir=/cloudsql \
      -instances="$CLOUD_SQL_INSTANCE"=tcp:5432 \
      -credential_file="$GOOGLE_APPLICATION_CREDENTIALS" > .db_proxy.log 2>&1 & echo $$! > .db_proxy.pid

    # Wait for the proxy to be ready
    tail -n +1 -f .db_proxy.log | sed '/ready for new connections/ q'

  PROXY_PID=$!

  echo "⏳ Waiting for Cloud SQL Proxy to become available..."
  
  # Install psql if needed
  apt-get update -qq && apt-get install -y -qq postgresql-client

  echo "🧪 Checking DB availability on localhost:5432..."

  # Wait and retry
  for i in $(seq 1 10); do
    PGPASSWORD=$POSTGRES_PASSWORD psql -h 127.0.0.1 -p 5432 -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c '\q' 2>/dev/null
    if [ $? -eq 0 ]; then
      echo "✅ Successfully connected to Cloud SQL via proxy!"
      break
    else
      echo "⏳ Attempt $i: Still waiting for DB to be ready..."
      sleep 2
    fi
  done

  # Final check
  PGPASSWORD=$POSTGRES_PASSWORD psql -h 127.0.0.1 -p 5432 -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c '\q' 2>/dev/null
  if [ $? -ne 0 ]; then
    echo "❌ ERROR: Could not connect to database after 10 tries."
    kill $PROXY_PID
    exit 1
  fi
fi

# Keep container alive (or start your app here)
echo "✅ Cloud SQL Proxy active, DB reachable. Container ready."
tail -f /dev/null
