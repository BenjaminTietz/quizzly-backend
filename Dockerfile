# ============================
# Builder stage
# ============================
FROM python:3.11-slim AS builder
# ============================
# Environment
# ============================
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Build dependencies (only here!)
RUN apt-get update && apt-get install -y \
    build-essential \
    ffmpeg \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# ============================
# Runtime stage (small!)
# ============================
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Runtime deps only
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libpq5 \
    postgresql-client \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy python packages only
COPY --from=builder /usr/local/lib/python3.11 /usr/local/lib/python3.11
COPY --from=builder /usr/local/bin /usr/local/bin

# ============================
# Copy project
# ============================

COPY . .
# ============================
# Entrypoint
# ============================
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
# ============================
# Static files
# ============================RUN mkdir -p /app/staticfiles
# ============================
# Expose port
# ============================
EXPOSE 8000
ENTRYPOINT ["/entrypoint.sh"]
