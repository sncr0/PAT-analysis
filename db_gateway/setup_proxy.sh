#!/bin/sh

echo "📦 DB Gateway container booting in MODE=$MODE"
echo "instance name: $CLOUD_SQL_INSTANCE_CONNECTION_NAME"



echo "🔌 Starting Cloud SQL Proxy for $CLOUD_SQL_INSTANCE_CONNECTION_NAME..."
rm -f .db_proxy.log .db_proxy.pid
stdbuf -oL /cloud_sql_proxy $CLOUD_SQL_INSTANCE_CONNECTION_NAME \
  --credentials-file=config/gcp-creds.json \
  --address=0.0.0.0 \
  --port=5432 > .db_proxy.log 2>&1 & echo $$! > .db_proxy.pid
tail -n +1 -f .db_proxy.log | sed '/ready for new connections/ q'

PROXY_PID=$!

echo "⏳ Waiting for Cloud SQL Proxy to become available..."


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

echo "✅ Cloud SQL Proxy active, DB reachable. Container ready."