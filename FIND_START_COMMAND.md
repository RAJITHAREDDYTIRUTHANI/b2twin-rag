# 🔍 Where to Find Start Command in Render

## ⚠️ **You're in the Wrong Section!**

The screenshot shows **"Docker Command"** - but you need **"Start Command"** for a Python web service.

---

## ✅ **Correct Location:**

### **Step 1: Go to the Right Section**

1. In Render dashboard → Your service (`biosphere2-rag`)
2. Click **"Settings"** tab (you're already here)
3. **Scroll down** past the Docker section
4. Look for **"Build & Deploy"** section

### **Step 2: Find "Start Command"**

In the **"Build & Deploy"** section, you'll see:

- **Build Command**: `pip install -r requirements_rag.txt`
- **Start Command**: ← **THIS IS WHAT YOU NEED TO EDIT!**

---

## 🔧 **How to Edit Start Command:**

1. Find the **"Start Command"** field in **"Build & Deploy"** section
2. Click the **"Edit"** button (pencil icon) next to it
3. Change it to:
   ```
   gunicorn spectacular_rag_web_app:app --bind 0.0.0.0:$PORT
   ```
4. Click **"Save Changes"**

---

## 📍 **Alternative: Check Service Type**

If you don't see "Start Command", your service might be configured as Docker:

1. Go to **Settings** → Scroll to top
2. Check **"Service Type"** or **"Runtime"**
3. Should be: **"Web Service"** or **"Python"**
4. If it says **"Docker"**, you need to change it

---

## 🎯 **Quick Checklist:**

- [ ] Go to Settings tab
- [ ] Scroll to "Build & Deploy" section (NOT Docker section)
- [ ] Find "Start Command" field
- [ ] Click "Edit"
- [ ] Set to: `gunicorn spectacular_rag_web_app:app --bind 0.0.0.0:$PORT`
- [ ] Save changes
- [ ] Trigger manual redeploy

---

**The Start Command is in the "Build & Deploy" section, not the Docker section!** 🚀


