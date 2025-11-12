# 🚨 URGENT: Fix Render Deployment

## **Problem:**
- ❌ Still seeing old UI ("Biosphere 2 Sensor Analysis")
- ❌ Still getting model error (`claude-3-5-sonnet-20241022`)

## **Solution: Force Redeploy on Render**

### **Step 1: Check Render Dashboard**
1. Go to: **https://dashboard.render.com**
2. Click your service: **`biosphere2-rag`**

### **Step 2: Verify Start Command**
1. Click **"Settings"** tab
2. Scroll to **"Start Command"**
3. **MUST BE:**
   ```
   gunicorn spectacular_rag_web_app:app --bind 0.0.0.0:$PORT
   ```
4. If it's different (like `web_app:app`), **CHANGE IT NOW!**

### **Step 3: Force Redeploy**
1. Click **"Manual Deploy"** button (top right)
2. Select **"Deploy latest commit"**
3. Click **"Deploy"**
4. **Wait 5-10 minutes** for deployment

### **Step 4: Verify It's Working**
After deployment completes (green "Live" status):

1. **Check the UI:**
   - ✅ Should see: **"Biosphere 2 RAG Analysis"** (neon cyberpunk design)
   - ❌ NOT: "Biosphere 2 Sensor Analysis"

2. **Test a question:**
   - Ask: "What is the temperature range?"
   - Should get AI response (no model error)

3. **Check browser console (F12):**
   - Network tab → Should call `/api/ask` (not `/ask`)

---

## **If Still Not Working:**

### **Check Render Logs:**
1. In Render dashboard → Click **"Logs"** tab
2. Look for startup message:
   - ✅ `Starting Spectacular Biosphere 2 RAG-Powered Web Interface...` = CORRECT
   - ❌ `Starting Biosphere 2 Sensor Analysis...` = WRONG FILE

### **If Wrong File:**
1. Settings → Start Command
2. Change to: `gunicorn spectacular_rag_web_app:app --bind 0.0.0.0:$PORT`
3. Save
4. Manual Deploy → Deploy latest commit

---

## **Quick Checklist:**
- [ ] Start Command = `gunicorn spectacular_rag_web_app:app --bind 0.0.0.0:$PORT`
- [ ] Manual redeploy triggered
- [ ] Deployment completed (green status)
- [ ] UI shows "Biosphere 2 RAG Analysis"
- [ ] No model error

**Do this NOW and it should work!** 🚀


