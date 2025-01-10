FROM python:3.10-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    netcat-openbsd \
    curl \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt . 
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Add a non-root user
RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser
USER appuser

# Expose application port
EXPOSE 8000

# Add health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Simplified ENTRYPOINT for inline logic
ENTRYPOINT ["/bin/bash", "-c", "\
    set -euo pipefail && \
    echo \"Checking database connectivity to ${DATABASE_HOST:-db}:${DATABASE_PORT:-5432}...\" && \
    start_time=$(date +%s) && \
    while true; do \
        if nc -z \"${DATABASE_HOST:-db}\" \"${DATABASE_PORT:-5432}\"; then \
            echo \"Database is up and reachable!\"; \
            break; \
        else \
            current_time=$(date +%s) && \
            elapsed=$(( current_time - start_time )) && \
            if [ \"$elapsed\" -ge \"${DB_WAIT_TIMEOUT:-30}\" ]; then \
                echo \"ERROR: Timed out after ${DB_WAIT_TIMEOUT:-30} seconds waiting for the database.\" >&2; \
                exit 1; \
            fi; \
            echo \"Database is unavailable - sleeping for 1 second...\"; \
            sleep 1; \
        fi; \
    done && \
    echo \"Running database migrations...\" && \
    python manage.py migrate --noinput && \
    echo \"Collecting static files...\" && \
    python manage.py collectstatic --noinput && \
    echo \"Starting the application...\" && \
    exec \"$@\" \
"]

# Default command
CMD ["gunicorn", "hsatracker.wsgi:application", "--bind", "0.0.0.0:8000"]
