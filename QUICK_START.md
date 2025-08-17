# 🚀 Quick Start - Deploy in 5 Minutes

## ⚡ **Super Quick Deployment**

### 1. **Push to GitHub** (2 minutes)
```bash
git add .
git commit -m "Ready for deployment"
git push origin main
```

### 2. **Deploy Frontend** (2 minutes)
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with GitHub
3. Click "New app"
4. Select: `concept-vote-sim` repository
5. Set main file: `app/dashboard.py`
6. Click "Deploy!"

### 3. **Deploy Backend** (1 minute)
1. Go to [render.com](https://render.com)
2. Click "New +" → "Web Service"
3. Connect your GitHub repo
4. Set start command: `uvicorn api.main:app --host 0.0.0.0 --port $PORT`
5. Add environment variable: `OPENAI_API_KEY=your_key_here`
6. Click "Create Web Service"

## 🎯 **What You Get**

- ✅ **Frontend**: `https://your-app-name.streamlit.app`
- ✅ **Backend**: `https://your-app-name.onrender.com`
- ✅ **Cost**: $0/month
- ✅ **Auto-deploy**: Updates on every git push

## 🔑 **Environment Variables**

### Streamlit Cloud
```
API_BASE=https://your-app-name.onrender.com
```

### Render
```
OPENAI_API_KEY=sk-your-key-here
MODEL=gpt-4o-mini
DEFAULT_VOTERS=100
```

## 🚨 **Common Issues**

- **API timeout**: Render free tier has 15-min limit
- **CORS errors**: Already handled in code
- **Missing dependencies**: Check requirements.txt

## 📖 **Need More Details?**

See the full [DEPLOYMENT.md](DEPLOYMENT.md) guide for complete instructions.

---

**🎉 You're ready to deploy! Run the deployment script:**
```bash
./deploy.sh
```
