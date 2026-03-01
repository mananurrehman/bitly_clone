# Stage 1: Build Stage (install dependencies)
FROM python:3.11-alpine AS builder

WORKDIR /app

RUN apk add --no-cache-dir --prefix=/install -r requirements.txt

# Stage 2: Final Stage (only runtime)
FROM python:3.11-alpine

WORKDIR /app 

COPY --from=builder /install /usr/local

COPY . .

EXPOSE 5000

CMD ["python", "run.py"]
