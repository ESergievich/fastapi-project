#!/bin/bash

# Запускаем миграции Alembic
poetry run alembic upgrade head

# Запускаем FastAPI
poetry run uvicorn main:app --host 0.0.0.0 --port 8000
