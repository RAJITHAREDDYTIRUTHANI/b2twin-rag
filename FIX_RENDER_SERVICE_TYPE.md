# 🔧 Fix Render Service Type & Start Command

## ⚠️ **Problem:**

Your service appears to be configured as **Docker** (showing Dockerfile Path, Docker Command, etc.), but it should be a **Python Web Service** with a Start Command.

---

## ✅ **Solution: Check Service Type**

### **Step 1: Check Service Type**

1. In Render dashboard → Your service (`biosphere2-rag`)
2. Go to **Settings** tab
3. **Scroll to the very top** of the Settings page
4. Look for **"Service Type"** or **"Runtime"** or **"Environment"**

**It should say:**
- ✅ **"Python"** or **"Web Service"** or **"Python 3"**
- ❌ **NOT "Docker"**

---

## 🔄 **If Service Type is Docker:**

### **Option A: Change Service Type (Recommended)**

1. You may need to **delete and recreate** the service as Python
2. OR check if there's a way to change the service type in Settings

### **Option B: Use Docker Command (Quick Fix)**

If you can't change the service type, set the **"Docker Command"** field to:

```
gunicorn spectacular_rag_web_app:app --bind 0.0.0.0:$PORT
```

But this is not ideal - the service should be Python, not Docker.

---

## ✅ **If Service Type is Python:**

### **Find Start Command:**

1. In **Settings** → **Build & Deploy** section
2. **Scroll down** past all the Docker fields
3. Look for:
   - **"Build Command"**: `pip install -r requirements_rag.txt`
   - **"Start Command"**: ← **THIS IS WHAT YOU NEED!**

4. Click **"Edit"** next to **"Start Command"**
5. Set it to:
   ```
   gunicorn spectacular_rag_web_app:app --bind 0.0.0.0:$PORT
   ```
6. Click **"Save Changes"**

---

## 🎯 **Quick Action:**

**First, check the top of Settings page:**
- What does it say for **"Service Type"** or **"Runtime"**?
- Is it **"Docker"** or **"Python"**?

**Then:**
- If **Python**: Find "Start Command" field and edit it
- If **Docker**: Either change service type OR set "Docker Command" as a temporary fix

---

## 📝 **What Your Service Should Look Like:**

**Service Type:** Python / Web Service  
**Build Command:** `pip install -r requirements_rag.txt`  
**Start Command:** `gunicorn spectacular_rag_web_app:app --bind 0.0.0.0:$PORT`  
**Environment Variables:** `ANTHROPIC_API_KEY` (set)

---

**Check the top of your Settings page and tell me what the Service Type says!** 🔍


