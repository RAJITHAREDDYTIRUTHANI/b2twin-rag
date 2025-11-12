# 🚀 Local Testing Guide

## ✅ **App is Starting!**

The Flask app is now running in the background.

### **Access Your App:**
Open your browser and go to:
```
http://localhost:5000
```

---

## 🧪 **What to Test:**

### **1. Check the UI:**
- ✅ Should see: **"Biosphere 2 RAG Analysis"** (neon cyberpunk design)
- ✅ Dark background with neon colors
- ✅ Subtitle: "Advanced AI-Powered Sensor Data Intelligence"

### **2. Test a Question:**
Try asking:
- "What is the temperature range?"
- "How many sensor readings were recorded?"
- "What is the fan status?"

### **3. Check Browser Console (F12):**
- Go to **Network** tab
- Ask a question
- Should call: `/api/ask` endpoint
- Should get response (no errors)

---

## ⚠️ **If You See Errors:**

### **Error: "RAG system is still initializing"**
- **Normal!** Wait 30-60 seconds for models to load
- Refresh the page after waiting

### **Error: "ANTHROPIC_API_KEY not found"**
- Make sure you have a `.env` file with:
  ```
  ANTHROPIC_API_KEY=your_api_key_here
  ```

### **Error: Module not found**
- Install dependencies:
  ```bash
  pip install -r requirements_rag.txt
  ```

---

## 🛑 **To Stop the App:**

Press `Ctrl+C` in the terminal, or close the terminal window.

---

## 📝 **Expected Behavior:**

1. **First Load:** Takes 30-60 seconds (loading ML models)
2. **Subsequent Loads:** Fast (models cached)
3. **Questions:** Should get AI-powered responses
4. **UI:** Beautiful neon cyberpunk design

**Your app should be running at: http://localhost:5000** 🎉

