# ──────────────────────────────────────────
# Stage 1: Builder
# ──────────────────────────────────────────
FROM python:3.11-alpine AS builder

WORKDIR /app

RUN apk add --no-cache gcc musl-dev linux-headers

COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# ──────────────────────────────────────────
# Stage 2: Final
# ──────────────────────────────────────────
FROM python:3.11-alpine

WORKDIR /app

COPY --from=builder /install /usr/local

COPY . .

EXPOSE 5000

CMD ["python", "run.py"]
