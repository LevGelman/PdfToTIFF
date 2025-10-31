# Poppler Installation Fix for Azure - Summary

## The Problem

Your Azure Web App shows this error:
```
PDFInfoNotInstalledError: Unable to get page count. Is poppler installed and in PATH?
```

**Root Cause**: Azure Web App's startup.sh cannot install poppler-utils because:
- No sudo/root access in startup scripts
- apt-get requires elevated privileges
- System packages can't be installed at runtime

## The Solution

**Use Docker deployment with poppler pre-installed in the container image.**

This ensures poppler-utils is already installed when the container starts.

---

## Quick Fix (Recommended)

### Option A: Automated Script

```bash
# Edit configuration in the script first
nano deploy_azure.sh

# Change these values:
ACR_NAME="your-unique-acr-name"      # Must be globally unique!
RESOURCE_GROUP="pdf-converter-rg"
APP_NAME="your-app-name"

# Run the script
./deploy_azure.sh
```

The script will:
1. ✅ Create Azure Container Registry
2. ✅ Build Docker image with poppler
3. ✅ Push image to ACR
4. ✅ Create/update Web App
5. ✅ Configure everything automatically

**Time**: ~10 minutes

### Option B: Manual Azure CLI

```bash
# 1. Create ACR
az acr create --name pdfconverteracr --resource-group pdf-converter-rg --sku Basic --admin-enabled true

# 2. Build and push image
az acr build --registry pdfconverteracr --image pdf-to-tiff:latest --file Dockerfile .

# 3. Create Web App
az webapp create \
  --resource-group pdf-converter-rg \
  --plan pdf-converter-plan \
  --name pdf-to-tiff-app \
  --deployment-container-image-name pdfconverteracr.azurecr.io/pdf-to-tiff:latest

# 4. Get ACR credentials
ACR_USERNAME=$(az acr credential show --name pdfconverteracr --query "username" -o tsv)
ACR_PASSWORD=$(az acr credential show --name pdfconverteracr --query "passwords[0].value" -o tsv)

# 5. Configure container
az webapp config container set \
  --name pdf-to-tiff-app \
  --resource-group pdf-converter-rg \
  --docker-custom-image-name pdfconverteracr.azurecr.io/pdf-to-tiff:latest \
  --docker-registry-server-url https://pdfconverteracr.azurecr.io \
  --docker-registry-server-user $ACR_USERNAME \
  --docker-registry-server-password $ACR_PASSWORD

# 6. Set environment variables
az webapp config appsettings set \
  --name pdf-to-tiff-app \
  --resource-group pdf-converter-rg \
  --settings SECRET_KEY="$(openssl rand -hex 32)" WEBSITES_PORT="8000"

# 7. Enable logging
az webapp log config \
  --name pdf-to-tiff-app \
  --resource-group pdf-converter-rg \
  --docker-container-logging filesystem

# 8. Restart
az webapp restart --name pdf-to-tiff-app --resource-group pdf-converter-rg
```

**Time**: ~15 minutes

### Option C: Azure Portal

See detailed step-by-step instructions in [AZURE_DOCKER_DEPLOY.md](AZURE_DOCKER_DEPLOY.md) - Method 2

**Time**: ~20 minutes

---

## What's Different Now?

### Before (Not Working ❌)
```
Azure Web App
  ├─ Python Runtime
  ├─ startup.sh (tries apt-get install poppler-utils)
  └─ ❌ FAILS: No sudo access
```

### After (Working ✅)
```
Azure Web App
  └─ Docker Container
      ├─ Python 3.11
      ├─ poppler-utils (pre-installed)
      ├─ All Python packages
      └─ Your application
```

---

## Files Involved

### Dockerfile (Already created ✅)
Pre-installs poppler-utils during image build:
```dockerfile
FROM python:3.11-slim
RUN apt-get update && apt-get install -y poppler-utils
# ... rest of setup
```

### deploy_azure.sh (New ✅)
Automated deployment script that handles everything

### AZURE_DOCKER_DEPLOY.md (New ✅)
Complete documentation with multiple deployment methods

---

## Verification After Deployment

### 1. Wait for Container to Start (2-3 minutes)

### 2. Check Logs
```bash
az webapp log tail --name pdf-to-tiff-app --resource-group pdf-converter-rg
```

Look for:
```
✅ Successfully installed Flask...
✅ Starting Gunicorn...
```

### 3. Test the Application
1. Visit: `https://your-app-name.azurewebsites.net`
2. Upload your 2 PDF files
3. Convert to TIFF
4. Download and open
5. ✅ Should work perfectly now!

### 4. Verify Poppler (Optional)
```bash
# SSH into container
az webapp ssh --name pdf-to-tiff-app --resource-group pdf-converter-rg

# Check poppler
pdfinfo -v
# Should show: pdfinfo version 24.02.0
```

---

## Updating After Code Changes

```bash
# Rebuild and push image
az acr build --registry pdfconverteracr --image pdf-to-tiff:latest --file Dockerfile .

# Restart web app to pull new image
az webapp restart --name pdf-to-tiff-app --resource-group pdf-converter-rg
```

Or use the script:
```bash
./deploy_azure.sh
```

---

## Cost

**Monthly Costs**:
- Azure Container Registry (Basic): ~$5/month
- App Service Plan (B1): ~$13/month
- **Total**: ~$18/month

**One-time**: Free (uses Azure credits if you have them)

---

## Troubleshooting

### "Container failed to start"
```bash
# Check logs
az webapp log tail --name pdf-to-tiff-app --resource-group pdf-converter-rg
```

### "Still getting PDFInfoNotInstalledError"
```bash
# Verify Dockerfile has poppler installation
cat Dockerfile | grep poppler

# Rebuild image
az acr build --registry pdfconverteracr --image pdf-to-tiff:latest .
az webapp restart --name pdf-to-tiff-app --resource-group pdf-converter-rg
```

### "App not responding"
```bash
# Check if WEBSITES_PORT is set to 8000
az webapp config appsettings list --name pdf-to-tiff-app --resource-group pdf-converter-rg | grep WEBSITES_PORT
```

---

## Why This Works

✅ **Docker Image**:
- Built with poppler pre-installed
- Has root access during build
- Creates immutable image

✅ **Azure Container Registry**:
- Stores your Docker images
- Private registry for your apps
- Fast deployment

✅ **Web App for Containers**:
- Runs your Docker image
- Handles scaling, SSL, monitoring
- No need for runtime package installation

---

## Summary

1. ❌ **Old way**: Try to install poppler in startup.sh → FAILS
2. ✅ **New way**: Use Docker with poppler pre-installed → WORKS

**Next Step**: Choose Option A, B, or C above and deploy!

---

## Need Help?

- **Full details**: See [AZURE_DOCKER_DEPLOY.md](AZURE_DOCKER_DEPLOY.md)
- **Quick start**: Run `./deploy_azure.sh`
- **Manual steps**: Follow Option B above

Your app will work perfectly once deployed with Docker! 🎉
