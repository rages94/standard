FROM python:3.12.3-alpine

RUN apk update && apk add --no-cache \
    gcc \
    g++ \
    musl-dev \
    libc-dev \
    libffi-dev \
    build-base

COPY poetry.lock pyproject.toml ./
RUN pip install --upgrade pip poetry wheel \
    && poetry config virtualenvs.create false \
    && poetry install --no-dev \
    && rm -rf /root/.cache/pip \

COPY . /app/

RUN chmod +x entrypoint.sh