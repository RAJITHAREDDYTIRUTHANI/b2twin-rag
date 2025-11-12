# Vercel Deployment Optimizations

## Changes Made

### 1. **Lazy Loading (`api/index.py`)**
- Uses `importlib` to dynamically import the main Flask app only on first request
- Prevents heavy ML models (sentence-transformers, faiss) from loading during build/cold start
- Includes fallback app for graceful degradation

### 2. **Updated Dependencies (`requirements.txt`)**
- Fixed `faiss-cpu` version to `1.12.0` (compatible with Python 3.12)
- Removed unnecessary `torch` dependency
- Kept all essential packages

### 3. **Vercel Configuration (`vercel.json`)**
- Set max function duration to 60 seconds
- Specified Python 3.12
- Configured proper routing

## Known Limitations

### ⚠️ **Free Tier Constraints**
- **Memory**: Free tier has limited memory (~1GB). Large ML models may cause issues
- **Timeout**: Free tier functions timeout at 10 seconds (we set 60s but may be capped)
- **Cold Starts**: First request will be slow as models load
- **Build Size**: Large dependencies may cause build issues

### 🔧 **If Deployment Still Fails**

**Option 1: Upgrade to Pro Plan**
- More memory (up to 3008MB)
- Longer timeouts (up to 300s)
- Better for ML workloads

**Option 2: Use Alternative Platforms** (Already configured)
- **Render** - Better for long-running processes with ML
- **Railway** - More flexible resource limits
- **Fly.io** - Better for containers with ML models

**Option 3: Lightweight Version**
- Remove RAG features temporarily
- Use simple keyword search instead
- Add RAG later when on paid tier

## Testing

After deployment:
1. First request will be slow (model loading)
2. Subsequent requests should be faster
3. Check Vercel logs for any errors
4. Monitor function execution time

## Troubleshooting

If you see `SIGKILL`:
- Memory limit exceeded
- Try removing `sentence-transformers` or `faiss-cpu` temporarily
- Or use Render/Railway instead

If build fails:
- Check Vercel build logs
- Verify all dependencies in `requirements.txt`
- Ensure Python version compatibility


