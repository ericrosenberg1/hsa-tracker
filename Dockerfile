# Use the official Python slim image
FROM python:3.10-slim

# Set environment variables to avoid Python buffering and caching
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Set working directory inside the container
WORKDIR /app

# Install system dependencies, including netcat-openbsd
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy project files and entrypoint script into the container
COPY . .

# Ensure the entrypoint script is executable
RUN chmod +x /app/entrypoint.sh

# Expose the Django default port
EXPOSE 8000

# Set entrypoint
ENTRYPOINT ["./entrypoint.sh"]

# Set default command to run the application
CMD ["gunicorn", "hsatracker.wsgi:application", "--bind", "0.0.0.0:8000"]
