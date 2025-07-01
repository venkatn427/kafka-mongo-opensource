#!/bin/bash
set -e

# Run DB migrations and init Superset
superset db upgrade

# Create admin user (ignore error if already exists)
superset fab create-admin \
  --username admin \
  --firstname Superset \
  --lastname Admin \
  --email admin@superset.com \
  --password admin || true

superset init

# Run any additional initialization scripts if needed
/app/init.sh

exec "$@"
