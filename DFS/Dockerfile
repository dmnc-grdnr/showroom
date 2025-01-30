# Multi-stage Dockerfile: builder builds required environment and runtime executes python code
# The builder image, used to build the virtual environment
FROM python:3.11-bookworm AS builder

RUN pip install poetry==1.8.4

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1

WORKDIR /app

COPY pyproject.toml ./

RUN poetry install --no-cache

# The runtime image, used to just run the code provided its virtual environment
FROM python:3.11-slim-bookworm AS runtime

ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH"

COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

WORKDIR /app

COPY python /app/python
COPY data /app/data
