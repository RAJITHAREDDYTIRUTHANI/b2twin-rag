# 🚀 Deploying to Vercel

Your Biosphere 2 RAG app is now configured for Vercel deployment!

## ⚠️ Important Notes

Vercel has some limitations for this type of application:
- **Large files**: Your database (`biosphere2_rag.db`) and CSV files are excluded (see `.vercelignore`)
- **Cold starts**: Data loading happens on each cold start (may be slow)
- **Function timeout**: Vercel functions have execution time limits
- **Memory limits**: Large ML models (sentence-transformers, FAISS) may hit memory limits

## 📦 Deployment Steps

### Option 1: Vercel CLI (Recommended)

1. **Install Vercel CLI**:
   ```bash
   npm i -g vercel
   ```

2. **Login to Vercel**:
   ```bash
   vercel login
   ```

3. **Deploy**:
   ```bash
   vercel
   ```

4. **Set Environment Variable**:
   ```bash
   vercel env add ANTHROPIC_API_KEY
   ```
   Enter your API key when prompted.

5. **Deploy to Production**:
   ```bash
   vercel --prod
   ```

### Option 2: Vercel Dashboard

1. Go to [vercel.com](https://vercel.com)
2. Sign up/Login with GitHub
3. Click "New Project"
4. Import your repository
5. Vercel will auto-detect Python configuration
6. Add environment variable:
   - Key: `ANTHROPIC_API_KEY`
   - Value: Your Anthropic API key
7. Click "Deploy"

## 🔧 Configuration

Files created:
- `vercel.json` - Vercel configuration
- `api/index.py` - Serverless function wrapper
- `.vercelignore` - Files to exclude from deployment
- `requirements.txt` - Python dependencies

## ⚙️ Environment Variables

Required:
- `ANTHROPIC_API_KEY` - Your Anthropic Claude API key

Optional:
- `PYTHON_VERSION` - Python version (default: 3.11)

## 📊 Alternative Deployment Options

If you encounter issues with Vercel (large dependencies, memory limits), consider:

1. **Render** (Already configured) - Better for long-running processes
2. **Railway** (Already configured) - Good for databases and ML models
3. **Fly.io** (Already configured) - More flexible resource limits

## 🐛 Troubleshooting

### Issue: Build fails due to large dependencies
**Solution**: Consider using a lighter embedding model or splitting the app

### Issue: Function times out
**Solution**: Optimize data loading or use a database service instead of local SQLite

### Issue: Memory errors
**Solution**: Reduce model size or upgrade Vercel plan

### Issue: Database not found
**Solution**: The database needs to be generated on first run or use an external database service

## 📝 Next Steps

1. Deploy to Vercel
2. Test all endpoints
3. Monitor function logs
4. Optimize cold start times if needed

Your app will be available at: `https://your-project.vercel.app`
