# Use Python instead of Node
FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y libpq-dev gcc && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Expose the port (Flask/FastAPI usually use 5000 or 8000)
EXPOSE 5000

CMD ["python", "run.py"]