# F1 Free Plan - Your Options

## The Problem

**F1 Free plan does NOT support Docker containers** ❌

Azure F1 (Free) limitations:
- ❌ No Docker/container support
- ❌ Only supports Python runtime (Oryx buildpack)
- ❌ Cannot install system packages like poppler-utils
- ❌ Your app won't work on F1

## Your Options

---

## ✅ Option 1: Upgrade to B1 Plan (~$13/month) - RECOMMENDED

### Why B1?
- ✅ Supports Docker containers
- ✅ Can install poppler-utils
- ✅ More memory (1.75GB vs 1GB)
- ✅ Better performance
- ✅ No daily execution limits
- ✅ Your app will work perfectly

### Cost Breakdown
| Item | Monthly Cost |
|------|-------------|
| Azure Container Registry (Basic) | ~$5 |
| App Service Plan B1 | ~$13 |
| **Total** | **~$18/month** |

### How to Upgrade

**Via Azure Portal:**
1. Go to your App Service Plan
2. Click "Scale up (App Service plan)"
3. Select **B1 Basic**
4. Click "Apply"

**Via Azure CLI:**
```bash
az appservice plan update \
  --name pdf-converter-plan \
  --resource-group pdf-converter-rg \
  --sku B1
```

Then deploy with Docker using `./deploy_azure.sh`

---

## ✅ Option 2: Azure Container Instances (Pay-per-use)

**Cheaper alternative** - Pay only when container is running!

### Pricing
- ~$0.01 per hour (1 vCPU, 1.5GB RAM)
- If used 8 hours/day = ~$2.50/month
- If used constantly = ~$7.50/month

### Pros:
- ✅ Much cheaper for occasional use
- ✅ Supports Docker
- ✅ Poppler works fine
- ✅ Easy to start/stop

### Cons:
- ❌ No built-in domain (need to use IP or setup custom domain)
- ❌ Container stops when idle (need to restart)
- ❌ No auto-scaling

### Deploy to ACI:

```bash
# Build and push image to ACR first
az acr create --name pdfconverteracr --resource-group pdf-converter-rg --sku Basic --admin-enabled true
az acr build --registry pdfconverteracr --image pdf-to-tiff:latest --file Dockerfile .

# Get ACR credentials
ACR_PASSWORD=$(az acr credential show --name pdfconverteracr --query "passwords[0].value" -o tsv)

# Create container instance
az container create \
  --resource-group pdf-converter-rg \
  --name pdf-to-tiff-container \
  --image pdfconverteracr.azurecr.io/pdf-to-tiff:latest \
  --cpu 1 \
  --memory 1.5 \
  --registry-login-server pdfconverteracr.azurecr.io \
  --registry-username pdfconverteracr \
  --registry-password $ACR_PASSWORD \
  --dns-name-label pdf-to-tiff-$(whoami) \
  --ports 8000 \
  --environment-variables SECRET_KEY="$(openssl rand -hex 32)"

# Get public URL
az container show \
  --resource-group pdf-converter-rg \
  --name pdf-to-tiff-container \
  --query ipAddress.fqdn \
  --output tsv
```

Access via: `http://pdf-to-tiff-yourname.region.azurecontainer.io:8000`

---

## ✅ Option 3: Use Azure Free Credits

If you have a new Azure account:
- ✅ $200 free credits (first 30 days)
- ✅ Use B1 plan for free during trial
- ✅ 12 months free services (but limited)

After credits expire, you can decide to continue or stop.

---

## ✅ Option 4: Alternative Free Platforms

### Render.com (Free Tier)
- ✅ Supports Docker
- ✅ Free tier available
- ✅ Auto-sleep after 15 min inactivity
- ⚠️ Slower startup (30-60 seconds)

```bash
# Create render.yaml
services:
  - type: web
    name: pdf-to-tiff
    runtime: docker
    plan: free
    envVars:
      - key: SECRET_KEY
        generateValue: true
```

Deploy via GitHub integration.

### Railway.app (Free Tier)
- ✅ $5 free credits/month
- ✅ Supports Docker
- ✅ Easy deployment

### Fly.io (Free Tier)
- ✅ 3 shared-cpu VMs free
- ✅ Supports Docker
- ✅ Better performance

Deploy:
```bash
# Install flyctl
curl -L https://fly.io/install.sh | sh

# Login
fly auth login

# Deploy
fly launch
```

---

## ❌ Option 5: Try Custom Buildpack on F1 (NOT RECOMMENDED)

**This is very unreliable and may not work!**

You can try creating a custom Oryx post-build script:

Create `.oryx-post-build.sh`:
```bash
#!/bin/bash
echo "Attempting to download poppler binaries..."

# Download pre-compiled poppler binaries
wget https://github.com/oschwartz10612/poppler-windows/releases/download/v23.01.0-0/Release-23.01.0-0.zip
unzip Release-23.01.0-0.zip -d /tmp/poppler
export PATH="/tmp/poppler/Library/bin:$PATH"

echo "Poppler installed to: /tmp/poppler"
```

Add to `startup.sh`:
```bash
#!/bin/bash
export PATH="/tmp/poppler/Library/bin:$PATH"
gunicorn --bind=0.0.0.0:8000 --timeout 600 --workers=2 app:app
```

**Problems**:
- ❌ May not work on Linux
- ❌ Binaries may not be compatible
- ❌ Gets reset on every deployment
- ❌ Very unreliable

---

## 📊 Cost Comparison

| Option | Monthly Cost | Reliability | Setup Difficulty |
|--------|-------------|-------------|------------------|
| **F1 Free** | $0 | ❌ Won't work | N/A |
| **B1 Basic (Docker)** | ~$18 | ✅ Excellent | Easy |
| **Container Instances** | ~$2-8 | ✅ Good | Medium |
| **Azure Free Credits** | $0 (30 days) | ✅ Excellent | Easy |
| **Render/Railway/Fly** | $0-5 | ⚠️ Good | Medium |
| **F1 Custom Buildpack** | $0 | ❌ Unreliable | Hard |

---

## 💡 My Recommendation

### For Development/Testing:
1. **Use Azure Free Credits** ($200 for 30 days)
   - Deploy with B1 + Docker
   - Test thoroughly
   - Decide if you want to continue

### For Personal/Light Use:
2. **Azure Container Instances**
   - Pay-per-use (~$2-8/month)
   - Stop when not using
   - Cheaper than B1

### For Production/Business:
3. **B1 Basic Plan** (~$18/month)
   - Most reliable
   - Best performance
   - Always available

### For Hobby Projects:
4. **Render.com or Fly.io**
   - Free tier available
   - Auto-sleep when idle
   - Good enough for demos

---

## 🚀 Quick Start (Recommended Path)

### If you're NEW to Azure:
```bash
# You probably have $200 free credits!
# Use B1 plan with Docker - it's FREE during trial

# 1. Check your credits
az account show --query "{Subscription:name, State:state}"

# 2. Deploy with Docker
./deploy_azure.sh

# You'll have 30 days to decide if you want to continue
```

### If credits expired:
```bash
# Option A: Upgrade to B1 (~$18/month)
az appservice plan update --name pdf-converter-plan --resource-group pdf-converter-rg --sku B1
./deploy_azure.sh

# Option B: Use Container Instances (~$2-8/month)
# See commands in Option 2 above

# Option C: Try Render.com (free)
# Push code to GitHub
# Connect to Render.com
# Deploy from GitHub
```

---

## ⚠️ Important Notes

### F1 Free Plan Reality:
- **Cannot run this app** - needs system packages
- **Very limited** - 60 CPU minutes/day
- **Slow** - 1GB RAM, shared CPU
- **Not for production**

### Why Docker Costs More:
- Docker needs more resources
- ACR storage costs money
- Better isolation and security
- More reliable deployments

### Reducing Costs:
1. **Stop when not using**: Delete resources, redeploy when needed
2. **Use Container Instances**: Only pay when running
3. **Use free platforms**: Render, Railway, Fly.io
4. **Share costs**: If for business, split among team

---

## 🎯 What to Do Now

1. **Check if you have Azure free credits**:
   ```bash
   az account show
   ```
   Look for "Free Trial" or new account status

2. **Choose your option**:
   - Free trial? → Use B1 with Docker (Option 1)
   - Want cheapest? → Container Instances (Option 2)
   - Want free forever? → Render/Fly.io (Option 4)

3. **Deploy according to your choice**

---

## Summary

**F1 Free Plan**: ❌ Cannot run your app (no Docker support)

**Best Option**:
- If new to Azure → Use free credits with B1 + Docker
- If light usage → Container Instances ($2-8/month)
- If production → B1 Basic ($18/month)
- If hobby → Render/Fly.io (free tier)

**My Recommendation**: Start with Azure free credits (B1 + Docker), test thoroughly, then decide what to do after 30 days.

---

Need help choosing? Let me know your usage pattern:
- How often will you use it?
- Is this for business or personal?
- Do you need it always available?
