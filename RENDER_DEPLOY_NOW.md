# 🚀 Deploy to Render - Step by Step

## ✅ **Changes Pushed to GitHub!**
- Commit: `06555f4` - "Working local version - Claude API integrated, model fixed, UI updated"
- Repository: `https://github.com/RAJITHAREDDYTIRUTHANI/b2twin-rag`

---

## 🔗 **Connect to Render (If Not Already Connected)**

### **Step 1: Go to Render Dashboard**
1. Open: **https://dashboard.render.com**
2. Sign in with your GitHub account

### **Step 2: Create/Update Web Service**

#### **If You Already Have a Service:**
1. Click on your service: **`biosphere2-rag`**
2. Go to **Settings** tab
3. Verify these settings:

**Start Command:**
```
gunicorn spectacular_rag_web_app:app --bind 0.0.0.0:$PORT
```

**Build Command:**
```
pip install -r requirements_rag.txt
```

**Environment Variables:**
- ✅ `ANTHROPIC_API_KEY` (must be set!)

4. Click **"Manual Deploy"** → **"Deploy latest commit"**
5. Wait 5-10 minutes

#### **If Creating New Service:**
1. Click **"New +"** → **"Web Service"**
2. Connect your GitHub repository:
   - Repository: `RAJITHAREDDYTIRUTHANI/b2twin-rag`
   - Branch: `main`
3. Configure:
   - **Name**: `biosphere2-rag`
   - **Region**: Choose closest to you
   - **Branch**: `main`
   - **Root Directory**: (leave empty)
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements_rag.txt`
   - **Start Command**: `gunicorn spectacular_rag_web_app:app --bind 0.0.0.0:$PORT`
4. Add Environment Variable:
   - Key: `ANTHROPIC_API_KEY`
   - Value: Your Anthropic API key
5. Click **"Create Web Service"**
6. Wait 5-10 minutes for first deployment

---

## ✅ **Verify Deployment**

### **After Deployment Completes (Green "Live" Status):**

1. **Check Logs:**
   - Go to **"Logs"** tab
   - Should see: `Starting Spectacular Biosphere 2 RAG-Powered Web Interface...`

2. **Visit Your App:**
   - URL will be: `https://biosphere2-rag.onrender.com` (or your custom name)
   - Should see: **"Biosphere 2 RAG Analysis"** (neon cyberpunk UI)

3. **Test It:**
   - Ask: "What is the temperature range?"
   - Should get AI response (no errors)

---

## 🎯 **Quick Checklist:**

- [ ] Render service created/updated
- [ ] Start Command = `gunicorn spectacular_rag_web_app:app --bind 0.0.0.0:$PORT`
- [ ] Build Command = `pip install -r requirements_rag.txt`
- [ ] `ANTHROPIC_API_KEY` environment variable set
- [ ] Manual deploy triggered (or auto-deploy from GitHub)
- [ ] Deployment completed (green "Live" status)
- [ ] App URL working
- [ ] UI shows "Biosphere 2 RAG Analysis"
- [ ] Questions work without errors

---

## 🐛 **Troubleshooting**

### **If Auto-Deploy Doesn't Work:**
1. Go to Settings → Build & Deploy
2. Make sure **"Auto-Deploy"** is enabled
3. Or manually trigger: **"Manual Deploy"** → **"Deploy latest commit"**

### **If You See Old UI:**
1. Clear browser cache (Ctrl+Shift+Delete)
2. Hard refresh (Ctrl+F5)
3. Check Render logs to confirm correct file is running

### **If Model Error:**
1. Verify `ANTHROPIC_API_KEY` is set in Render environment variables
2. Check Render logs for API errors

---

## 🎉 **Success!**

Once deployed, your app will be live at:
```
https://biosphere2-rag.onrender.com
```

**Share this URL with your team!** 🚀


