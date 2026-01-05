FROM python:3.11-slim

WORKDIR /app

# Optional: nicer Python defaults
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install dependencies
RUN pip install --no-cache-dir fastapi "uvicorn[standard]" pika

# Copy project files into the container
COPY . .

# Default command (producer app); docker compose can override if needed
CMD ["uvicorn", "producer_app.main:app", "--host", "0.0.0.0", "--port", "8000"]
