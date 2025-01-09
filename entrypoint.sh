#!/bin/bash
set -euo pipefail

# Function to display messages with timestamp
log() {
  echo "[$(date +'%Y-%m-%dT%H:%M:%S%z')] $@"
}

# Function to check database readiness with timeout
wait_for_db() {
  local host="$1"
  local port="$2"
  local timeout="${3:-30}"  # Default timeout is 30 seconds
  local start_time=$(date +%s)

  log "Checking database connectivity to ${host}:${port}..."

  while true; do
    if nc -z "${host}" "${port}"; then
      log "Database is up and reachable!"
      break
    else
      current_time=$(date +%s)
      elapsed=$(( current_time - start_time ))
      if [ "${elapsed}" -ge "${timeout}" ]; then
        log "ERROR: Timed out after ${timeout} seconds waiting for the database."
        exit 1
      fi
      log "Database is unavailable - sleeping for 1 second..."
      sleep 1
    fi
  done
}

# Main execution function
main() {
  # Read database host and port from environment variables, with defaults
  DATABASE_HOST="${DATABASE_HOST:-db}"
  DATABASE_PORT="${DATABASE_PORT:-5432}"
  DB_WAIT_TIMEOUT="${DB_WAIT_TIMEOUT:-30}"  # Optional: Allow overriding timeout via .env

  # Wait for the database to be ready
  wait_for_db "${DATABASE_HOST}" "${DATABASE_PORT}" "${DB_WAIT_TIMEOUT}"

  # Run database migrations
  log "Running database migrations..."
  python manage.py migrate --noinput

  # Collect static files
  log "Collecting static files..."
  python manage.py collectstatic --noinput

  # Start the application using the command passed to the container
  log "Starting the application..."
  exec "$@"
}

# Execute the main function
main
