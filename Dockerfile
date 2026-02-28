FROM python:3.12-slim as builder
WORKDIR /install
RUN apt-get update && apt-get install -y build-essential libpq-dev && pip install poetry==1.8.5
COPY poetry.lock* pyproject.toml ./
RUN poetry export -f requirements.txt --without-hashes --output requirements.txt && \
    pip install --upgrade pip && \
    pip wheel --no-deps --wheel-dir /wheels -r requirements.txt

FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1
WORKDIR /app
RUN apt-get update && apt-get install curl -y
COPY --from=builder /wheels /wheels
COPY --from=builder /install/requirements.txt .
RUN pip install --no-deps --no-index --find-links=/wheels -r requirements.txt
COPY . .
CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0"]