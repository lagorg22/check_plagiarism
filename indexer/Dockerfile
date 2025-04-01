FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y curl git && apt-get clean

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create shared directory structure
RUN mkdir -p /app/shared/codefiles /app/shared/processed_codefiles /app/shared/embeddings && \
    chmod -R 777 /app/shared

# Expose port (if needed for health checks, otherwise can be removed)
EXPOSE 8001

# Default command - just keep container running
CMD ["tail", "-f", "/dev/null"] 