#!/bin/bash

echo "Applying Migrations"
poetry run alembic upgrade head

echo "Starting FastAPI..."
poetry run uvicorn --host 0.0.0.0 --port $PORT --log-level 'debug' "$@" main:create_app
#uvicorn --env-file './.env' --host 0.0.0.0 --port 8000 --workers 9 --log-level 'debug' "$@" run:create_app
