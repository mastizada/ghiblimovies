FROM python:3.8.6-alpine3.12 AS base_image

WORKDIR /app/

ENV PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100

# install all build tools and save packages to a local virtual environment folder
FROM base_image as builder
RUN apk update && apk add gcc libffi-dev musl-dev postgresql-dev && pip install poetry && \
    poetry config virtualenvs.create true && poetry config virtualenvs.in-project true

COPY poetry.lock pyproject.toml ./
RUN poetry install --no-root --no-dev

# copy the virtual environment file to the final image
FROM base_image as runner

# libpq is required by psycopg2-binary plugin
RUN apk add libpq

COPY ./ /app
COPY --from=builder /app/.venv /app/.venv

ENV PYTHONPATH=/app

CMD ["/app/.venv/bin/gunicorn", "ghiblimovies.wsgi", "--bind", "0:8000"]
