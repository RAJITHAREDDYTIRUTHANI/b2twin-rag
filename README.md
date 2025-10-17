# 🌿 Biosphere 2 Sensor Analysis Web App

A modern, interactive web application for analyzing Biosphere 2 environmental sensor data using AI-powered natural language processing.

## ✨ Features

- **Interactive Chat Interface**: Ask questions about your sensor data in natural language
- **Real-time Analysis**: Get instant, crisp answers from Claude AI
- **Sensor Overview**: Visual dashboard showing all sensor systems
- **Quick Questions**: Pre-built questions for common queries
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Production Ready**: Optimized for Jetstream2 deployment

## 🚀 Quick Start (Local Development)

1. **Install Dependencies**:
   ```bash
   pip install flask anthropic pandas python-dotenv
   ```

2. **Set up Environment**:
   ```bash
   # Create .env file with your Anthropic API key
   echo "ANTHROPIC_API_KEY=your_api_key_here" > .env
   ```

3. **Run the Application**:
   ```bash
   python web_app.py
   ```

4. **Open in Browser**:
   ```
   http://localhost:5000
   ```

## 🌐 Jetstream2 Deployment

### Option 1: Direct Deployment

1. **Upload Files to Jetstream2**:
   ```bash
   scp -r . username@your-jetstream2-instance:/home/username/biosphere2-app/
   ```

2. **SSH into Instance**:
   ```bash
   ssh username@your-jetstream2-instance
   ```

3. **Install Dependencies**:
   ```bash
   cd biosphere2-app
   pip install -r requirements_production.txt
   ```

4. **Run Application**:
   ```bash
   python production_app.py
   ```

### Option 2: Docker Deployment

1. **Build Docker Image**:
   ```bash
   docker build -t biosphere2-app .
   ```

2. **Run Container**:
   ```bash
   docker run -d -p 5000:5000 --name biosphere2-app biosphere2-app
   ```

3. **Access Application**:
   ```
   http://your-jetstream2-ip:5000
   ```

### Option 3: Gunicorn Production Server

1. **Use Deployment Script**:
   ```bash
   chmod +x deploy.sh
   ./deploy.sh
   ```

## 📊 Data Structure

The application analyzes 6 sensor systems:

- **Temperature Sensor**: 507 readings (Sept 21-28, 2025)
- **Fan Direction**: 2 readings
- **Fan Output**: 507 readings  
- **Fan Status**: 2 readings
- **Valve Commands**: 2 readings
- **Valve Limits**: 2 readings

## 🎯 Sample Questions

- "What's the temperature range?"
- "How many readings were recorded?"
- "What's the fan status?"
- "Are there any errors?"
- "What's the highest temperature?"
- "What's the monitoring period?"

## 🔧 Configuration

### Environment Variables

- `ANTHROPIC_API_KEY`: Your Anthropic API key (required)
- `FLASK_ENV`: Set to `production` for production deployment
- `FLASK_APP`: Set to `production_app.py` for production

### File Structure

```
biosphere2-app/
├── web_app.py              # Development version
├── production_app.py       # Production version
├── simple_interface.py     # Core analysis functions
├── requirements_production.txt
├── Dockerfile
├── deploy.sh
├── data/                   # CSV sensor data files
├── results/               # Generated analysis files
└── logs/                  # Application logs
```

## 🛠️ API Endpoints

- `GET /`: Main web interface
- `POST /ask`: Submit questions (JSON: `{"question": "your question"}`)
- `GET /api/data`: Get sensor data as JSON
- `GET /api/status`: Check system status

## 📱 Features

- **Modern UI**: Clean, responsive design with gradient backgrounds
- **Real-time Chat**: Instant AI responses with loading indicators
- **Quick Questions**: Click-to-ask common questions
- **Sensor Dashboard**: Visual overview of all sensor systems
- **Mobile Friendly**: Responsive design for all devices
- **Error Handling**: Graceful error handling and user feedback

## 🔒 Security Notes

- API keys are loaded from environment variables
- Production version disables debug mode
- Gunicorn provides production-grade WSGI server
- Docker container runs with minimal privileges

## 📈 Performance

- **Background Data Loading**: Sensor data loads in background thread
- **Cached Responses**: Context data is cached for faster responses
- **Optimized Prompts**: Ultra-crisp responses (200 token limit)
- **Production Server**: Gunicorn with 4 workers for scalability

## 🚀 Ready for Production!

This application is production-ready and optimized for:
- ✅ Local development
- ✅ Jetstream2 cloud deployment  
- ✅ Docker containerization
- ✅ Scalable production hosting

**Start asking questions about your Biosphere 2 sensor data!** 🌿
