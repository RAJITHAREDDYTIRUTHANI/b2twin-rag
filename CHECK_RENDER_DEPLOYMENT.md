# 🔍 Check Render Deployment - Troubleshooting Guide

## ⚠️ **Issue: Still Seeing Old UI and Model Error**

You're seeing:
- ❌ Old UI: "Biosphere 2 Sensor Analysis" / "Interactive Environmental Monitoring System"
- ❌ Error: `claude-3-5-sonnet-20241022` not found

This means **Render hasn't deployed the new code yet** or is using the wrong file.

---

## 🔧 **Step 1: Verify Render Configuration**

1. Go to: **https://dashboard.render.com**
2. Click on your service: **`biosphere2-rag`**
3. Go to **Settings** tab
4. Check **Start Command** - should be:
   ```
   gunicorn spectacular_rag_web_app:app --bind 0.0.0.0:$PORT
   ```
5. If it's different, **update it** and save

---

## 🔄 **Step 2: Force Redeploy**

### **Option A: Manual Redeploy (Recommended)**
1. In Render dashboard → Your service
2. Click **"Manual Deploy"** button (top right)
3. Select **"Deploy latest commit"**
4. Wait ~5 minutes

### **Option B: Trigger via Git Push**
If Render is connected to GitHub:
```bash
# Make a small change to trigger redeploy
git commit --allow-empty -m "Trigger Render redeploy"
git push origin main
```

---

## ✅ **Step 3: Verify Deployment**

After redeploy completes:

1. **Check Logs** in Render dashboard:
   - Should see: `Starting Spectacular Biosphere 2 RAG-Powered Web Interface...`
   - Should NOT see: `Starting Biosphere 2 Sensor Analysis Web Interface...`

2. **Check the UI**:
   - ✅ Should see: **"Biosphere 2 RAG Analysis"** (not "Sensor Analysis")
   - ✅ Should see: **"Advanced AI-Powered Sensor Data Intelligence"** (not "Interactive Environmental Monitoring System")
   - ✅ Should have neon cyberpunk design (dark background, neon colors)

3. **Test API**:
   - Open browser console (F12)
   - Ask a question
   - Check Network tab → Should call `/api/ask` (not `/ask`)

---

## 🐛 **If Still Not Working:**

### **Check Which File is Running:**

1. **Check Render Logs** - Look for startup message:
   - ✅ `Starting Spectacular Biosphere 2 RAG-Powered Web Interface...` = Correct
   - ❌ `Starting Biosphere 2 Sensor Analysis Web Interface...` = Wrong file

2. **Check Start Command** in Render Settings:
   - Must be: `gunicorn spectacular_rag_web_app:app --bind 0.0.0.0:$PORT`
   - If it says `web_app:app` or `flask_interface:app`, **change it!**

3. **Check GitHub Connection**:
   - Render → Settings → Build & Deploy
   - Make sure it's connected to the right repo
   - Make sure branch is `main`

---

## 📝 **Quick Fix Checklist:**

- [ ] Render Start Command = `gunicorn spectacular_rag_web_app:app --bind 0.0.0.0:$PORT`
- [ ] Manual redeploy triggered
- [ ] Deployment completed (green "Live" status)
- [ ] UI shows "Biosphere 2 RAG Analysis" (not "Sensor Analysis")
- [ ] API calls `/api/ask` (not `/ask`)
- [ ] No more model error

---

## 🚨 **If Render is Using Wrong File:**

If Render is somehow using `web_app.py` instead:

1. **Update render.yaml** (already correct, but verify):
   ```yaml
   startCommand: gunicorn spectacular_rag_web_app:app --bind 0.0.0.0:$PORT
   ```

2. **Or manually set in Render Dashboard**:
   - Settings → Start Command
   - Change to: `gunicorn spectacular_rag_web_app:app --bind 0.0.0.0:$PORT`
   - Save and redeploy

---

**After fixing, your app should work!** 🎉


