# syntax=docker/dockerfile:1
FROM python:3.12

ENV PYTHONDONTWRITEBYTECODE=1

ENV PYTHONUNBUFFERED=1

RUN pip3.12 install --upgrade pip
# RUN pip install poetry

ENV POETRY_VIRTUALENVS_IN_PROJECT=true

RUN python3.12 -m venv .venv
ENV PATH="/.venv/bin:$PATH"

WORKDIR /app

# COPY pyproject.toml poetry.lock /app/

# RUN poetry install --no-root

COPY requirements.txt /app/

RUN pip3.12 install --no-cache-dir -r requirements.txt

COPY . /app/