# Biosphere 2 Sensor Analysis Web App
# Docker configuration for Jetstream2 deployment

FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies (needed for sentence-transformers and faiss)
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements_rag.txt .
RUN pip install --no-cache-dir -r requirements_rag.txt

# Copy application files
COPY spectacular_rag_web_app.py .
COPY simple_interface.py .
COPY rag_database.py .
COPY data/ ./data/
COPY static/ ./static/

# Create necessary directories
RUN mkdir -p logs

# Set environment variables
ENV FLASK_APP=spectacular_rag_web_app.py
ENV FLASK_ENV=production

# Expose port (Render uses $PORT)
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/ || exit 1

# Run the application (Render will override with $PORT)
CMD ["gunicorn", "--bind", "0.0.0.0:${PORT:-5000}", "--workers", "2", "--timeout", "300", "spectacular_rag_web_app:app"]
