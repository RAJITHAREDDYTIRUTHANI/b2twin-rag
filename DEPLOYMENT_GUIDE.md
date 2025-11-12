# 🚀 Biosphere 2 RAG Deployment Guide

Deploy your RAG-powered sensor analysis system to the cloud and share it with your friends!

## 🌟 Quick Deploy Options

### Option 1: Render.com (Recommended - Free & Easy)

**Steps:**
1. Go to https://render.com
2. Sign up with GitHub (connect your repo)
3. Click "New" → "Web Service"
4. Connect your repository: `https://github.com/RAJITHAREDDYTIRUTHANI/b2twin-rag`
5. Configure:
   - **Name**: `biosphere2-rag`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements_rag.txt`
   - **Start Command**: `gunicorn spectacular_rag_web_app:app --bind 0.0.0.0:$PORT`
   - **Environment Variables**:
     - `ANTHROPIC_API_KEY`: Your Anthropic API key
6. Click "Create Web Service"
7. Wait for deployment (first time takes ~5 minutes)

**Your app will be live at**: `https://biosphere2-rag.onrender.com`

---

### Option 2: Railway (Fast & Simple)

**Steps:**
1. Go to https://railway.app
2. Sign up with GitHub
3. Click "New Project" → "Deploy from GitHub"
4. Select `b2twin-rag` repository
5. Add environment variable:
   - `ANTHROPIC_API_KEY`: Your key
6. Railway auto-detects Flask and deploys!

**Your app will be live at**: `https://biosphere2-rag-production.up.railway.app`

---

### Option 3: Fly.io (Good for Global Access)

**Steps:**
1. Install Fly CLI: https://fly.io/docs/getting-started/installing-flyctl/
2. Create account: `fly auth signup`
3. In project directory: `fly launch`
4. Add secrets: `fly secrets set ANTHROPIC_API_KEY=your_key`
5. Deploy: `fly deploy`

**Your app will be live at**: `https://biosphere2-rag.fly.dev`

---

## 🔧 Environment Variables

All platforms require your Anthropic API key:

```
ANTHROPIC_API_KEY=sk-ant-api03-...
```

**Get your key from**: https://console.anthropic.com/

---

## 📊 What Gets Deployed

✅ **Core Files**:
- `spectacular_rag_web_app.py` - Main Flask app
- `rag_database.py` - RAG system
- `data/*.csv` - Sensor data files
- `requirements_rag.txt` - Dependencies

✅ **Already Configured**:
- `render.yaml` - Render.com config
- `Procfile` - Heroku/Railway config
- `runtime.txt` - Python version
- `.gitignore` - Clean repository

---

## 🎨 Features Available

Your deployed app includes:
- 🌈 Amazing neon cyberpunk UI
- 🤖 RAG-powered semantic search
- 📊 Multi-sensor data analysis
- 💬 Interactive Q&A interface
- 📈 Real-time statistics

---

## 🔗 Sharing Your App

Once deployed, share your app URL:
- **Render**: `https://biosphere2-rag.onrender.com`
- **Railway**: `https://biosphere2-rag-production.up.railway.app`
- **Fly.io**: `https://biosphere2-rag.fly.dev`

**Example message**:
```
Hey! Check out my Biosphere 2 sensor analysis AI:
🔗 https://biosphere2-rag.onrender.com

You can ask it questions like:
- "What's the temperature range?"
- "When did the fan turn on?"
- "Show me valve operations"
```

---

## 🛠️ Troubleshooting

### Issue: "API key not found"
**Solution**: Add `ANTHROPIC_API_KEY` environment variable in your platform settings

### Issue: "Database error"
**Solution**: The SQLite database is auto-created on first run. Wait a minute after first deploy.

### Issue: "Slow first load"
**Solution**: First load builds RAG index (~30 seconds). Subsequent loads are instant!

### Issue: "Module not found"
**Solution**: Check `requirements_rag.txt` has all dependencies

---

## 💰 Free Tier Limits

- **Render**: 750 hours/month free
- **Railway**: $5 free credit monthly
- **Fly.io**: Generous free tier

All are perfect for sharing with friends! 🎉

---

## 🎯 Next Steps

1. Deploy to your preferred platform
2. Test your app
3. Share the URL with friends
4. Monitor usage in dashboard

**Happy Deploying!** 🚀✨




