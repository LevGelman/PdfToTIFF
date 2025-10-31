# Deploy to Render.com - FREE Forever! 🎉

## Perfect for Your Pet Project

✅ **Completely FREE**
✅ Supports Docker with poppler
✅ No credit card required
✅ Auto-deploys from GitHub
✅ HTTPS included
✅ Easy setup (10 minutes)

## How Render Free Tier Works

### Pros:
- ✅ 100% FREE forever
- ✅ 512MB RAM (enough for small PDFs)
- ✅ Shared CPU
- ✅ Supports Docker
- ✅ Automatic HTTPS
- ✅ Custom domains (optional)

### Limitations:
- ⚠️ Auto-sleeps after 15 min of inactivity
- ⚠️ First request after sleep takes 30-60 seconds to wake up
- ⚠️ Less memory than paid plans (fine for 2-3 PDFs at a time)
- ⚠️ Shared resources (slower than dedicated)

**Perfect for**: Pet projects, demos, occasional use

---

## Quick Deploy (5 Steps)

### Step 1: Push Code to GitHub

```bash
# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "PDF to TIFF converter ready for Render deployment"

# Create repo on GitHub (do this in browser first)
# Then add remote and push:
git remote add origin https://github.com/YOUR_USERNAME/PdfToTIFF.git
git branch -M main
git push -u origin main
```

### Step 2: Sign Up for Render

1. Go to https://render.com
2. Click **"Get Started for Free"**
3. Sign up with GitHub (easiest)
4. Authorize Render to access your repositories

### Step 3: Create New Web Service

1. Click **"New +"** → **"Web Service"**
2. Connect your GitHub repository: `PdfToTIFF`
3. Click **"Connect"**

### Step 4: Configure Service

Render will auto-detect `render.yaml` and use these settings:

- **Name**: `pdf-to-tiff-converter` (or change it)
- **Runtime**: Docker
- **Plan**: Free
- **Branch**: main

Click **"Create Web Service"**

### Step 5: Wait for Build

- First build takes 5-10 minutes
- Watch the logs in real-time
- When you see: ✅ **"Your service is live"**
- Click the URL to access your app!

**Done!** 🎉

---

## Your App URL

Render gives you a free URL:
```
https://pdf-to-tiff-converter.onrender.com
```

Or with your custom name:
```
https://your-chosen-name.onrender.com
```

---

## Configuration Files (Already Created ✅)

### 1. render.yaml ✅
Already created! Tells Render how to deploy.

### 2. Dockerfile ✅
Already exists! Has poppler pre-installed.

### 3. .dockerignore ✅
Already exists! Optimizes build.

**You're all set!** Just push to GitHub and connect to Render.

---

## Step-by-Step with Screenshots

### 1. Create GitHub Repo

**Option A: GitHub CLI** (if installed)
```bash
gh repo create PdfToTIFF --public --source=. --remote=origin --push
```

**Option B: GitHub Website**
1. Go to https://github.com/new
2. Name: `PdfToTIFF`
3. Public or Private (both work)
4. Click "Create repository"
5. Follow instructions to push existing repo:
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/PdfToTIFF.git
   git branch -M main
   git push -u origin main
   ```

### 2. Connect to Render

1. **Sign in**: https://dashboard.render.com
2. **New Web Service**: Click "New +" → "Web Service"
3. **Connect Repo**:
   - If first time: Click "Connect account" → Authorize GitHub
   - Select your repository: `PdfToTIFF`
   - Click "Connect"

### 3. Configure (Auto-detected from render.yaml)

Render reads `render.yaml` automatically:

```yaml
Name: pdf-to-tiff-converter
Runtime: Docker
Plan: Free ✅
Environment: SECRET_KEY (auto-generated) ✅
```

Click **"Create Web Service"**

### 4. Watch Deployment

You'll see build logs in real-time:

```
==> Building Docker image
==> Installing system dependencies
==> Installing poppler-utils ✅
==> Installing Python packages
==> Build successful
==> Starting service
==> Your service is live 🎉
```

**First build**: 5-10 minutes
**Subsequent builds**: 2-3 minutes

### 5. Test Your App

1. Click the URL: `https://your-app.onrender.com`
2. Upload your 2 PDFs
3. Convert to TIFF
4. Download and verify!

---

## Auto-Deploy on Code Changes

**Every time you push to GitHub, Render auto-deploys!**

```bash
# Make changes to your code
nano app.py

# Commit and push
git add .
git commit -m "Updated feature"
git push

# Render automatically:
# 1. Detects the push
# 2. Builds new image
# 3. Deploys new version
# 4. No downtime!
```

---

## Managing Your App

### View Logs
Dashboard → Your Service → Logs

### Restart Service
Dashboard → Your Service → Manual Deploy → "Deploy latest commit"

### Environment Variables
Dashboard → Your Service → Environment → Add Variable

### Custom Domain (Optional)
Dashboard → Your Service → Settings → Custom Domain

---

## Important: Free Tier Behavior

### Auto-Sleep
- App sleeps after **15 minutes** of inactivity
- First request after sleep takes **30-60 seconds** to wake up
- Subsequent requests are fast
- This is normal for free tier!

### What User Sees:
1. Visits your URL
2. Sees "Service is waking up..." (30-60 sec)
3. App loads normally
4. Stays awake for 15 minutes

### Keeping It Awake (Optional):
Use a free uptime monitor to ping every 10 minutes:
- https://uptimerobot.com (free)
- Ping your URL every 10 minutes
- App never sleeps!

**Setup UptimeRobot**:
1. Sign up free
2. Add Monitor → HTTP(s)
3. URL: `https://your-app.onrender.com/health`
4. Interval: 10 minutes
5. Done!

---

## Troubleshooting

### Build Fails
Check logs for errors:
- Missing files? → Ensure all files are committed
- Dockerfile issues? → Verify Dockerfile syntax
- Python errors? → Check requirements.txt

### App Doesn't Start
Check logs for:
```bash
# Should see:
✅ Starting gunicorn 23.0.0
✅ Listening at: http://0.0.0.0:8000

# If you see errors, check:
- PORT environment variable (should be 8000)
- SECRET_KEY is set
- All dependencies installed
```

### "Service Unavailable"
- App is sleeping → Wait 30-60 seconds
- App crashed → Check logs
- Build failed → Check build logs

### Memory Errors
Free tier has 512MB RAM:
- Process smaller PDFs (< 10MB each)
- Reduce DPI to 150 or 200
- Don't upload too many files at once

### Slow Performance
Free tier uses shared CPU:
- Normal for free tier
- First request after sleep is slowest
- Upgrade to paid plan ($7/mo) for better performance

---

## Upgrading (Optional)

If you need better performance:

**Starter Plan**: $7/month
- ✅ No sleep
- ✅ 512MB RAM (same as free)
- ✅ Faster CPU
- ✅ Always available

**Standard Plan**: $25/month
- ✅ 2GB RAM
- ✅ More CPU
- ✅ Better for larger files

**For now**: Stick with FREE! ✅

---

## Render vs Azure Comparison

| Feature | Render Free | Azure B1 |
|---------|-------------|----------|
| **Cost** | $0 | $18/month |
| **Memory** | 512MB | 1.75GB |
| **CPU** | Shared | Dedicated |
| **Sleep** | Yes (15 min) | No |
| **Setup** | 10 min | 30 min |
| **Docker** | ✅ Yes | ✅ Yes |
| **Poppler** | ✅ Works | ✅ Works |
| **Auto-deploy** | ✅ Yes | Manual |
| **HTTPS** | ✅ Free | ✅ Free |

**For pet project**: Render Free is perfect! ✅

---

## Alternative Free Platforms

If you want to compare:

### Fly.io
- Free: 3 shared VMs
- 256MB RAM each
- Better performance than Render
- More complex setup

### Railway
- Free: $5 credits/month
- ~100 hours/month
- Easy setup
- Runs out after free credits

### Render (Current Choice)
- Free: Forever
- Auto-sleep after 15 min
- Easiest setup
- Best for beginners

**Recommendation**: Start with Render (easiest)

---

## Quick Commands Reference

```bash
# Initial setup
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/PdfToTIFF.git
git push -u origin main

# Update app
git add .
git commit -m "Updated feature"
git push

# View logs (via Render dashboard)
# https://dashboard.render.com → Your Service → Logs

# Restart service (via Render dashboard)
# https://dashboard.render.com → Your Service → Manual Deploy
```

---

## What Happens Next

1. ✅ You push code to GitHub
2. ✅ Render detects the push
3. ✅ Builds Docker image (5-10 min first time)
4. ✅ Deploys automatically
5. ✅ Your app is live!
6. ✅ URL: `https://your-app.onrender.com`
7. ✅ 100% FREE forever!

---

## Summary

**Cost**: $0 (FREE forever) ✅
**Setup Time**: 10 minutes ✅
**Difficulty**: Easy ✅
**Supports Docker**: Yes ✅
**Poppler Works**: Yes ✅
**Perfect For**: Pet projects ✅

---

## Need Help?

### Render Documentation
- https://render.com/docs/docker
- https://render.com/docs/deploy-from-github

### Render Community
- https://community.render.com

### This Project
- Check [README.md](README.md) for app details
- Check [Dockerfile](Dockerfile) for build config
- Check [render.yaml](render.yaml) for Render config

---

## Ready to Deploy?

1. ✅ Read this guide
2. ✅ Push code to GitHub
3. ✅ Sign up for Render (free)
4. ✅ Connect repository
5. ✅ Click "Create Web Service"
6. ✅ Wait 5-10 minutes
7. ✅ Your app is live!

**No credit card needed. 100% FREE forever!** 🎉

Start here: https://render.com/
