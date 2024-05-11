FROM python:3.11

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ENV POETRY_HOME=/opt/poetry
ENV POETRY_VIRTUALENVS_IN_PROJECT=true

ENV PATH="/app/.venv/bin:$PATH"

WORKDIR /app

COPY . .

RUN pip install poetry && \
    poetry install --no-interaction --no-ansi

WORKDIR /app/src