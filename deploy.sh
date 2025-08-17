#!/bin/bash

# 🚀 Concept Vote Simulator Deployment Script
# This script helps you deploy your app for free

echo "🚀 Concept Vote Simulator - Free Deployment"
echo "============================================="

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "❌ Git not initialized. Please run:"
    echo "   git init"
    echo "   git add ."
    echo "   git commit -m 'Initial commit'"
    exit 1
fi

# Check if remote origin exists
if ! git remote get-url origin > /dev/null 2>&1; then
    echo "❌ No remote origin found. Please add your GitHub repository:"
    echo "   git remote add origin https://github.com/YOUR_USERNAME/concept-vote-sim.git"
    exit 1
fi

echo "✅ Git repository ready"
echo ""

# Show current status
echo "📊 Current Status:"
echo "   Repository: $(git remote get-url origin)"
echo "   Branch: $(git branch --show-current)"
echo "   Last commit: $(git log -1 --oneline)"
echo ""

# Check for uncommitted changes
if [ -n "$(git status --porcelain)" ]; then
    echo "⚠️  You have uncommitted changes. Committing them now..."
    git add .
    git commit -m "Auto-commit before deployment"
fi

# Push to GitHub
echo "📤 Pushing to GitHub..."
git push origin main

echo ""
echo "🎉 Deployment initiated!"
echo ""
echo "📋 Next Steps:"
echo "1. Go to [share.streamlit.io](https://share.streamlit.io)"
echo "2. Sign in with GitHub"
echo "3. Click 'New app'"
echo "4. Select your repository: concept-vote-sim"
echo "5. Set main file path: app/dashboard.py"
echo "6. Click 'Deploy!'"
echo ""
echo "🌐 For the backend API:"
echo "1. Go to [render.com](https://render.com)"
echo "2. Create a new Web Service"
echo "3. Connect your GitHub repo"
echo "4. Set start command: uvicorn api.main:app --host 0.0.0.0 --port \$PORT"
echo ""
echo "🔑 Don't forget to set environment variables in both platforms!"
echo "   - OPENAI_API_KEY"
echo "   - API_BASE (in Streamlit Cloud)"
echo ""
echo "📖 Full deployment guide: DEPLOYMENT.md"
