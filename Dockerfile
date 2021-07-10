FROM python:3.9-slim

ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY ./.env.prod /.env 

RUN apt-get update \ 
    && apt-get install --no-install-recommends -y \
    build-essential \
    libpython3-dev \
    libpq-dev

RUN pip install poetry
COPY ./pyproject.toml /pyproject.toml

RUN poetry config virtualenvs.create false
RUN poetry install --no-dev

COPY ./app .