FROM python:3.11-slim

WORKDIR /app


ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install dependencies (Updated to include kafka-python)
RUN pip install --no-cache-dir fastapi "uvicorn[standard]" kafka-python

# Copy project files into the container
COPY . .

# Default command
CMD ["uvicorn", "producer_app.main:app", "--host", "0.0.0.0", "--port", "8000"]