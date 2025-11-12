# 🚀 Running on Localhost

## Quick Start

### **1. Start the Application**

```bash
python spectacular_rag_web_app.py
```

### **2. Open in Browser**

Once you see "Running on http://0.0.0.0:5000", open:

**http://localhost:5000**

---

## 📋 Prerequisites Check

### **Dependencies Installed?**
```bash
pip install -r requirements_rag.txt
```

**Required packages:**
- ✅ Flask
- ✅ sentence-transformers
- ✅ faiss-cpu
- ✅ anthropic
- ✅ pandas
- ✅ python-dotenv

### **API Key Set?**
Create a `.env` file in the project root:

```
ANTHROPIC_API_KEY=sk-ant-api03-...
```

**Or set environment variable:**
```bash
# Windows PowerShell
$env:ANTHROPIC_API_KEY="your_key_here"

# Windows CMD
set ANTHROPIC_API_KEY=your_key_here

# Linux/Mac
export ANTHROPIC_API_KEY=your_key_here
```

---

## 🎯 What Happens When You Start

1. **Initialization** (~5-10 seconds):
   - Loads sensor data from CSV files
   - Creates document chunks (31 chunks)
   - Generates embeddings (93 embeddings)
   - Builds FAISS vector index

2. **Server Starts**:
   - Flask server on `http://localhost:5000`
   - Background data loading continues

3. **Ready to Use**:
   - Web interface loads
   - System status shows "Ready"
   - Can start asking questions!

---

## 🌐 Access Points

### **Main Interface**
- **URL**: http://localhost:5000
- **What**: Interactive chat interface with neon cyberpunk UI

### **API Endpoints**
- **System Status**: http://localhost:5000/api/system-status
- **RAG Stats**: http://localhost:5000/api/rag-stats
- **Ask Question**: POST http://localhost:5000/api/ask

---

## 🔧 Troubleshooting

### **Port 5000 Already in Use?**
Change the port in `spectacular_rag_web_app.py`:

```python
app.run(host='0.0.0.0', port=5001, debug=True, threaded=True)
```

Then access: http://localhost:5001

### **Module Not Found Errors?**
```bash
pip install -r requirements_rag.txt
```

### **API Key Error?**
Make sure `.env` file exists with:
```
ANTHROPIC_API_KEY=your_actual_key
```

### **Database Not Found?**
The system will create `biosphere2_rag.db` automatically on first run.

### **Slow First Load?**
Normal! First run needs to:
- Load ML model (~30 seconds)
- Generate embeddings (~1-2 minutes)
- Build vector index (~5 seconds)

Subsequent runs are faster if database exists.

---

## ✅ Expected Console Output

```
Starting Spectacular Biosphere 2 RAG-Powered Web Interface...
Loading sensor data and initializing RAG database...
Web interface will be available at: http://localhost:5000
Amazing neon cyberpunk visual effects loading...
Loading Biosphere 2 sensor data...
[OK] temperature: 507 readings
[OK] fan_direction: 2 readings
...
[SUCCESS] Sensor data loaded!
Initializing RAG database...
[SUCCESS] RAG Database initialized: biosphere2_rag.db
[SUCCESS] Embedding model loaded: all-MiniLM-L6-v2
Creating document chunks...
Adding documents to RAG database...
[SUCCESS] Added 31 documents to RAG database
Building vector index...
[SUCCESS] Vector index built with 93 embeddings
[SUCCESS] RAG database ready!
 * Running on http://0.0.0.0:5000
 * Debug mode: on
```

---

## 🎮 Using the Interface

1. **Wait for "System Ready"** status (green indicator)
2. **Ask a question** in the chat box
3. **View sources** - see which documents informed the answer
4. **Check stats** - monitor RAG system metrics

### **Example Questions:**
- "What is the temperature range?"
- "How many fan readings are there?"
- "What are the valve system statuses?"
- "Show me the monitoring period"

---

## 🛑 Stopping the Server

Press `Ctrl + C` in the terminal to stop the server.

---

## 📝 Notes

- **First run**: Takes 1-2 minutes (model loading + embedding generation)
- **Subsequent runs**: Much faster (30 seconds) if database exists
- **Background loading**: Data loads in background, interface available immediately
- **Hot reload**: With debug=True, changes auto-reload the app

**Enjoy your RAG-powered Biosphere 2 sensor analysis system!** 🌿🧠



