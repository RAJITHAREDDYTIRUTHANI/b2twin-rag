# Biosphere 2 Sensor Analysis Web App
# Docker configuration for Jetstream2 deployment

FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements_production.txt .
RUN pip install --no-cache-dir -r requirements_production.txt

# Copy application files
COPY production_app.py .
COPY simple_interface.py .
COPY data/ ./data/
COPY results/ ./results/

# Create necessary directories
RUN mkdir -p logs

# Set environment variables
ENV FLASK_APP=production_app.py
ENV FLASK_ENV=production

# Expose port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/api/status || exit 1

# Run the application
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "--timeout", "120", "production_app:app"]
