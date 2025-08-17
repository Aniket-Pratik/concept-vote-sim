# 🚀 Free Deployment Guide

This guide will help you deploy your Concept Vote Simulator for free using Streamlit Cloud and Render.

## 📋 **Prerequisites**

1. **GitHub Account** (free)
2. **Streamlit Cloud Account** (free)
3. **Render Account** (free)
4. **OpenAI API Key** (you already have this)

## 🎯 **Deployment Strategy**

- **Frontend (Streamlit)**: Streamlit Cloud (free)
- **Backend (FastAPI)**: Render (free tier)
- **Database**: None needed (stateless app)

## 🔧 **Step 1: Prepare Your Repository**

### 1.1 Create a GitHub Repository

```bash
# Initialize git if not already done
git init
git add .
git commit -m "Initial commit: Concept Vote Simulator"

# Create a new repository on GitHub, then:
git remote add origin https://github.com/YOUR_USERNAME/concept-vote-sim.git
git branch -M main
git push -u origin main
```

### 1.2 Repository Structure

Your repository should look like this:
```
concept-vote-sim/
├── api/
│   ├── main.py
│   ├── models.py
│   ├── personas.py
│   ├── tally.py
│   └── vote.py
├── app/
│   └── dashboard.py
├── requirements.txt
├── .streamlit/
│   └── config.toml
├── .env.example
└── README.md
```

## 🌐 **Step 2: Deploy Backend API on Render**

### 2.1 Create Render Account
1. Go to [render.com](https://render.com)
2. Sign up with GitHub
3. Create a new account

### 2.2 Deploy FastAPI Service

1. **Click "New +" → "Web Service"**
2. **Connect your GitHub repository**
3. **Configure the service:**

```
Name: concept-vote-sim-api
Environment: Python 3
Build Command: pip install -r requirements.txt
Start Command: uvicorn api.main:app --host 0.0.0.0 --port $PORT
```

4. **Add Environment Variables:**
```
OPENAI_API_KEY=your_openai_api_key_here
MODEL=gpt-4o-mini
DEFAULT_VOTERS=100
```

5. **Click "Create Web Service"**

### 2.3 Get Your API URL
- Render will give you a URL like: `https://your-app-name.onrender.com`
- Copy this URL for the next step

## 🎨 **Step 3: Deploy Frontend on Streamlit Cloud**

### 3.1 Update API URL in Code

Before deploying, update the API URL in your Streamlit app:

```python
# In app/dashboard.py, change this line:
API = os.getenv("API_BASE", "https://your-app-name.onrender.com")
```

### 3.2 Deploy on Streamlit Cloud

1. **Go to [share.streamlit.io](https://share.streamlit.io)**
2. **Sign in with GitHub**
3. **Click "New app"**
4. **Configure:**

```
Repository: your-username/concept-vote-sim
Branch: main
Main file path: app/dashboard.py
```

5. **Click "Deploy!"**

### 3.3 Set Environment Variables

In Streamlit Cloud, go to your app settings and add:
```
API_BASE=https://your-app-name.onrender.com
```

## 🔄 **Step 4: Update and Deploy**

### 4.1 Make Changes
```bash
git add .
git commit -m "Update API URL for deployment"
git push
```

### 4.2 Automatic Deployment
- **Streamlit Cloud**: Automatically redeploys on push
- **Render**: Automatically redeploys on push

## 🌍 **Step 5: Custom Domain (Optional)**

### Streamlit Cloud
- Go to app settings
- Add custom domain
- Update DNS records

### Render
- Go to service settings
- Add custom domain
- Update DNS records

## 📱 **Step 6: Test Your Deployment**

1. **Test the API**: Visit your Render URL + `/healthz`
2. **Test the Frontend**: Visit your Streamlit Cloud URL
3. **Run a test**: Try the concept voting functionality

## 🚨 **Common Issues & Solutions**

### Issue: API Timeout
**Solution**: Render free tier has 15-minute timeout. For longer operations, consider:
- Reducing voter count
- Using faster models
- Implementing async processing

### Issue: CORS Errors
**Solution**: Already handled in the code with proper CORS settings

### Issue: Environment Variables Not Loading
**Solution**: Make sure to set them in both Streamlit Cloud and Render

## 💰 **Cost Breakdown**

- **Streamlit Cloud**: $0/month
- **Render**: $0/month (free tier)
- **OpenAI API**: Pay-per-use (you control costs)
- **Total**: $0/month hosting

## 🔒 **Security Considerations**

1. **API Key**: Never commit your OpenAI API key to GitHub
2. **Environment Variables**: Use platform environment variables
3. **Rate Limiting**: Consider adding rate limiting for production use
4. **CORS**: Properly configured for security

## 📈 **Scaling Up (When You're Ready)**

### Free Tier Limits
- **Streamlit Cloud**: 1GB RAM, 1 CPU
- **Render**: 750 hours/month, 512MB RAM

### Paid Options
- **Streamlit Cloud Pro**: $10/month (more resources)
- **Render**: $7/month (dedicated resources)
- **AWS/GCP**: Enterprise-grade hosting

## 🎉 **You're Done!**

Your Concept Vote Simulator is now:
- ✅ **Hosted for free**
- ✅ **Automatically deployed**
- ✅ **Accessible worldwide**
- ✅ **Professional-grade**

## 🔗 **Useful Links**

- [Streamlit Cloud](https://share.streamlit.io)
- [Render](https://render.com)
- [GitHub](https://github.com)
- [OpenAI API](https://platform.openai.com)

---

**Need help?** Check the troubleshooting section or create an issue in your GitHub repository.
