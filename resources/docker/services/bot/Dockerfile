#!/bin/sh
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install uv globally
RUN pip install --no-cache-dir uv

# Copy project files related to dependencies first for layer caching
COPY pyproject.toml .

# Create virtual environment inside the image
RUN uv venv
RUN uv lock
RUN uv sync

# Copy the rest of the application code
COPY . .
