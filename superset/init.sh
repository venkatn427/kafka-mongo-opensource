#!/bin/bash
# Initialize superset database and setup admin user, roles, etc.
superset db upgrade
superset fab create-admin --username admin --firstname Admin --lastname User --email admin@example.com --password admin
superset init
python /app/superset_setup.py
exec "$@"
