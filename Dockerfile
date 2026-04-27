# Dockerfile for Somn AI System
# Multi-stage build for production deployment

# ============================================================
# Stage 1: Base image with Python dependencies
# ============================================================
FROM python:3.13-slim AS base

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# ============================================================
# Stage 2: Build dependencies
# ============================================================
FROM base AS builder

COPY somn/requirements.txt .

RUN pip install --prefix=/install -r requirements.txt

# ============================================================
# Stage 3: Runtime image (base for all targets)
# ============================================================
FROM python:3.13-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Install minimal runtime deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && groupadd -r somn && useradd -r -g somn -d /app -s /sbin/nologin somn

WORKDIR /app

# Copy installed packages from builder
COPY --from=builder /install /usr/local

# Copy application code
COPY somn/ ./somn/
COPY Somn-GUI/ ./Somn-GUI/
COPY README.md LICENSE ./

# Create data directories
RUN mkdir -p /app/data/run \
             /app/data/logs \
             /app/data/knowledge \
             /app/data/core \
             /app/data/backups \
             /app/data/imperial_library \
    && chown -R somn:somn /app

USER somn

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8964/api/v1/health || exit 1

# ============================================================
# API target - FastAPI server
# ============================================================
FROM runtime AS api

EXPOSE 8964

CMD ["python", "somn/api/server.py"]

# ============================================================
# GUI target - Desktop application (requires display)
# ============================================================
FROM runtime AS gui

# Install GUI dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libxcb-cursor0 \
    libxkbcommon-x11-0 \
    libegl1 \
    libgl1 \
    libxcb-icccm4 \
    libxcb-image0 \
    libxcb-keysyms1 \
    libxcb-randr0 \
    libxcb-render-util0 \
    && rm -rf /var/lib/apt/lists/*

CMD ["python", "-m", "Somn-GUI"]
