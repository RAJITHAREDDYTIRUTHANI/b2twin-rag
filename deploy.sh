#!/bin/bash
# Deployment script for Jetstream2

echo "🌿 Deploying Biosphere 2 Sensor Analysis Web App to Jetstream2..."

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements_production.txt

# Set environment variables
echo "🔧 Setting up environment..."
export FLASK_APP=production_app.py
export FLASK_ENV=production

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p logs
mkdir -p results

# Start the application with Gunicorn
echo "🚀 Starting application..."
gunicorn --bind 0.0.0.0:5000 --workers 4 --timeout 120 --access-logfile logs/access.log --error-logfile logs/error.log production_app:app

echo "✅ Deployment complete!"
echo "🌐 Application available at: http://your-jetstream2-ip:5000"
