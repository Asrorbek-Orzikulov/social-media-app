# Builder image, used to build the virtual environment
FROM python:3.12.2 as builder

WORKDIR /app/

RUN pip install poetry==1.8.2

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

COPY pyproject.toml poetry.lock README.md ./

RUN poetry install --no-root && rm -rf $POETRY_CACHE_DIR

# Runtime image, used to just run the code provided its virtual environment
FROM python:3.12.2-slim as runtime

ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH"

COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

WORKDIR /app/

COPY . .

CMD [ "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000" ]