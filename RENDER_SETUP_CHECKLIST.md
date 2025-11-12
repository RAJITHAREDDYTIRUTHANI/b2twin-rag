# ✅ Render Deployment Checklist

## You've Connected to Render! Here's What to Configure:

### **1. Repository Connection** ✅
- [x] Connected your GitHub repository

### **2. Service Configuration**

In Render dashboard, make sure these settings match:

**Service Type**: Web Service  
**Name**: `biosphere2-rag` (or your choice)  
**Region**: Choose closest to you  
**Branch**: `main` (or your main branch)

### **3. Build & Start Commands**

Render should auto-detect from `render.yaml`, but verify:

**Build Command**: 
```
pip install -r requirements_rag.txt
```

**Start Command**:
```
gunicorn spectacular_rag_web_app:app --bind 0.0.0.0:$PORT
```

### **4. Environment Variables** ⚠️ **CRITICAL**

**You MUST add this environment variable:**

1. In Render dashboard, go to **Environment** section
2. Click **Add Environment Variable**
3. Add:
   - **Key**: `ANTHROPIC_API_KEY`
   - **Value**: Your actual API key (from https://console.anthropic.com/)
4. Click **Save Changes**

**Without this, the app will fail!**

### **5. Python Version**

Render will use Python 3.11 (from `render.yaml`)

---

## 🚀 Deployment Process

Once configured:

1. **Click "Create Web Service"**
2. **Wait 5-10 minutes** (first deployment takes longer):
   - Installing dependencies (~2-3 min)
   - Loading ML models (~1-2 min)
   - Building RAG database (~30 sec)
   - Starting server (~30 sec)

3. **Check deployment logs** for:
   - ✅ "Installing dependencies..."
   - ✅ "Loading embedding model..."
   - ✅ "RAG database ready!"
   - ✅ "Running on..."

---

## 🎯 Expected Deployment Timeline

```
0:00 - Build starts
0:30 - Dependencies installing (sentence-transformers, FAISS, etc.)
3:00 - Dependencies installed
3:30 - Application starting
4:00 - Loading sensor data...
4:30 - Building RAG database...
5:00 - Server running! ✅
```

**Total**: ~5-10 minutes for first deployment

---

## ✅ Success Indicators

You'll know it's working when:

1. **Deployment Status**: "Live" (green)
2. **Logs show**: 
   - `[SUCCESS] RAG database ready!`
   - `Running on http://0.0.0.0:XXXX`
3. **Visit URL**: Your app loads (may take 30 seconds on first visit)

---

## 🐛 Common Issues

### **Issue: Build fails - "Module not found"**
**Solution**: Make sure `requirements_rag.txt` has all dependencies

### **Issue: App starts but crashes**
**Solution**: Check logs - probably missing `ANTHROPIC_API_KEY`

### **Issue: "502 Bad Gateway" or timeout**
**Solution**: 
- First request takes time (loading ML models)
- Wait 30-60 seconds, then refresh
- Check logs for errors

### **Issue: "Application Error"**
**Solution**:
- Check environment variables (API key set?)
- Check build logs for errors
- Verify all files are in repository

---

## 📊 What Render Shows You

**Dashboard displays:**
- ✅ **Status**: Live, Building, or Error
- 📊 **Metrics**: CPU, Memory usage
- 📝 **Logs**: Real-time deployment logs
- 🔗 **URL**: Your app's public URL

---

## 🌐 Your App URL

Once deployed, your app will be at:
```
https://biosphere2-rag.onrender.com
```
(Or whatever name you chose)

---

## 🎉 Next Steps After Deployment

1. **Test the app**: Visit your URL
2. **Wait for initialization**: First load takes ~30 seconds
3. **Try a question**: "What is the temperature range?"
4. **Share with team**: Give them the URL!

---

## 📝 Quick Reference

**Files Render Uses:**
- ✅ `render.yaml` - Configuration (auto-detected)
- ✅ `requirements_rag.txt` - Dependencies
- ✅ `spectacular_rag_web_app.py` - Main app
- ✅ `rag_database.py` - RAG system
- ✅ `data/*.csv` - Sensor data (included in repo)

**Environment Variables Needed:**
- ✅ `ANTHROPIC_API_KEY` (required!)
- `PYTHON_VERSION` (auto-set from render.yaml)

**That's it! Your app should deploy successfully on Render!** 🚀


