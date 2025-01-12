FROM python:3.10-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    GUNICORN_WORKERS=3 \
    GUNICORN_TIMEOUT=120

WORKDIR /app

# Install dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    netcat-openbsd \
    curl \
    bash \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create a non-root user
RUN addgroup --system appgroup && \
    adduser --system --ingroup appgroup appuser && \
    chown -R appuser:appgroup /app

USER appuser

EXPOSE 4111

# Healthcheck to ensure the service is up
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:4111/health || exit 1

# Define the CMD, including database readiness, migrations, and static file collection
CMD /bin/bash -c "\
    echo 'Waiting for database...' && \
    until nc -z ${DATABASE_HOST} ${DATABASE_PORT}; do sleep 1; done && \
    echo 'Database is up' && \
    python manage.py migrate --noinput && \
    python manage.py collectstatic --noinput && \
    gunicorn hsatracker.wsgi:application \
    --bind 0.0.0.0:4111 \
    --workers ${GUNICORN_WORKERS} \
    --timeout ${GUNICORN_TIMEOUT} \
    --access-logfile - \
    --error-logfile - \
    --log-level debug"
