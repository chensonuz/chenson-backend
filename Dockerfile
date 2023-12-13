FROM python:3.10-buster

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app
COPY . /app

RUN pip install poetry
RUN poetry config --local virtualenvs.in-project true
RUN poetry install --with dev --no-interaction --no-root
# RUN poetry run pytest tests
