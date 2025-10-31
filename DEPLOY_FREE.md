# Deploy FREE - Quick Start

## 🎉 Render.com - 100% FREE Forever!

Perfect for your pet project! No credit card needed.

---

## ⚡ Quick Deploy (3 Steps)

### Step 1: Push to GitHub (2 minutes)

```bash
# In your project directory
git init
git add .
git commit -m "PDF to TIFF converter - ready for deployment"

# Create repo on GitHub (browser):
# 1. Go to https://github.com/new
# 2. Name: PdfToTIFF
# 3. Click "Create repository"

# Push code
git remote add origin https://github.com/YOUR_USERNAME/PdfToTIFF.git
git branch -M main
git push -u origin main
```

**Or use GitHub CLI**:
```bash
gh repo create PdfToTIFF --public --source=. --remote=origin --push
```

### Step 2: Deploy on Render (3 minutes)

1. Go to https://render.com
2. Click **"Get Started for Free"**
3. Sign up with GitHub
4. Click **"New +"** → **"Web Service"**
5. Connect repository: `PdfToTIFF`
6. Click **"Connect"**
7. Click **"Create Web Service"** (auto-detects settings)

### Step 3: Wait for Build (5-10 minutes)

Watch the logs. When you see:
```
✅ Your service is live
```

Click the URL and test your app!

**Done!** 🎉

---

## 📋 What You Get

✅ Free URL: `https://your-app.onrender.com`
✅ Auto HTTPS
✅ Auto-deploy on git push
✅ Docker with poppler installed
✅ 512MB RAM (enough for small PDFs)
✅ 100% FREE forever

---

## ⚠️ Free Tier Limitations

- **Auto-sleep**: After 15 min of inactivity
- **Wake-up time**: 30-60 seconds on first request
- **Memory**: 512MB (keep PDFs small)
- **CPU**: Shared (slower than paid)

**Perfect for**: Pet projects, demos, occasional use

---

## 🔄 Update Your App

```bash
# Make changes
nano app.py

# Push to GitHub
git add .
git commit -m "Updated feature"
git push

# Render auto-deploys! (2-3 minutes)
```

---

## 📖 Full Guide

See **[RENDER_DEPLOY.md](RENDER_DEPLOY.md)** for:
- Detailed setup instructions
- Troubleshooting
- Custom domains
- Keeping app awake (optional)
- Performance tips

---

## 💡 Tips

### Keep App Awake (Optional)
Use free UptimeRobot:
1. Sign up: https://uptimerobot.com
2. Add monitor to: `https://your-app.onrender.com/health`
3. Interval: 10 minutes
4. App never sleeps!

### Optimize for Free Tier
- Use DPI 150 or 200 (not 300/400)
- Upload max 2-3 small PDFs at once
- Keep individual PDFs under 10MB

---

## 🆘 Need Help?

- **Full Guide**: [RENDER_DEPLOY.md](RENDER_DEPLOY.md)
- **Render Docs**: https://render.com/docs/docker
- **Render Support**: https://community.render.com

---

## Summary

**Cost**: $0 (FREE) ✅
**Time**: 10 minutes total
**Difficulty**: Super easy
**Poppler**: Works perfectly ✅

Ready? Start at https://render.com 🚀
