FROM python:3.13-slim

WORKDIR /app

# Install system deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY pyproject.toml README.md AGENTS.md ARCHITECTURE.md ./
COPY src/ ./src/
COPY data/ ./data/

# Install Python deps
RUN pip install --no-cache-dir .

# Expose port
EXPOSE 4444

# Run the server
CMD ["python", "-m", "src.main"]
