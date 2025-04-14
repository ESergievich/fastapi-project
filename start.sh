#!/bin/bash

set -e

echo ">>> Running Alembic migrations..."
poetry run alembic upgrade head

if [ "${APP_CONFIG__INITIAL_DATA__SEED_DATA}" = "1" ]; then
  echo ">>> Seeding data..."
  poetry run python -m actions.seed
  poetry run python -m actions.create_superuser
else
  echo ">>> Skipping seed data."
fi

echo ">>> Starting FastAPI..."
poetry run uvicorn main:app --host 0.0.0.0 --port 8000
