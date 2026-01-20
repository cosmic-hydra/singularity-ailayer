# Note: This Dockerfile is for building/testing purposes
# Full functionality requires Windows with GUI access

FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY pyproject.toml .
COPY requirements.txt .
COPY core/ core/
COPY tests/ tests/

# Install Python dependencies
RUN pip install --no-cache-dir -e ".[dev]"

# Run tests (without Windows-specific features)
CMD ["pytest", "tests/", "-v", "--ignore=tests/test_windows_integration.py"]
