# Switch from Python Runtime to Docker - Step by Step

## Current Situation

Your Azure Web App is currently using **Python runtime** (not Docker), which is why poppler cannot be installed.

Evidence from your logs:
```
File "/opt/python/3.13.5/lib/python3.13/subprocess.py"
File "/tmp/8de18a2cb0b0842/antenv/lib/python3.13/site-packages/..."
```

This means Azure is using the **Python buildpack**, which doesn't allow system package installation.

---

## The Fix: Switch to Docker Deployment

You have **two options**: Recreate the app with Docker, or try installing poppler via Oryx buildpack (less reliable).

---

## ✅ Option 1: Recreate Web App with Docker (RECOMMENDED)

This is the cleanest and most reliable solution.

### Step 1: Delete Current Web App (Optional - keeps same URL)

**Via Azure Portal:**
1. Go to your Web App in Azure Portal
2. Click "Delete"
3. Confirm deletion

**OR via CLI:**
```bash
az webapp delete \
  --name pdf-to-tiff-app \
  --resource-group pdf-converter-rg
```

### Step 2: Run Automated Deployment Script

```bash
# Make sure you're in the project directory
cd /home/lev/Documents/repos/PdfToTIFF

# Edit configuration (IMPORTANT!)
nano deploy_azure.sh

# Change these values to match your setup:
ACR_NAME="pdfconverteracr"           # Make this unique globally
RESOURCE_GROUP="pdf-converter-rg"    # Your resource group name
APP_NAME="pdf-to-tiff-app"          # Your desired app name
LOCATION="eastus"                    # Your Azure region

# Save and exit (Ctrl+X, Y, Enter)

# Run the deployment
./deploy_azure.sh
```

**What it does:**
1. ✅ Creates Azure Container Registry
2. ✅ Builds Docker image with poppler installed
3. ✅ Pushes image to registry
4. ✅ Creates Web App with Docker container
5. ✅ Configures all settings
6. ✅ Starts the app

**Time:** ~10 minutes

### Step 3: Wait and Test

```bash
# Wait 2-3 minutes for container to start

# Check logs
az webapp log tail --name pdf-to-tiff-app --resource-group pdf-converter-rg

# Look for successful start:
# ✅ "Starting gunicorn"
# ✅ "Listening at: http://0.0.0.0:8000"

# Get your app URL
az webapp show --name pdf-to-tiff-app --resource-group pdf-converter-rg --query defaultHostName -o tsv
```

### Step 4: Test with Your PDFs

1. Visit your app URL
2. Upload your PDFs
3. Convert to TIFF
4. Download and verify it works! ✅

---

## ⚙️ Option 2: Manual Azure CLI (If Script Fails)

```bash
# Set variables
ACR_NAME="pdfconverteracr"
RESOURCE_GROUP="pdf-converter-rg"
APP_NAME="pdf-to-tiff-app"
LOCATION="eastus"
APP_PLAN="pdf-converter-plan"

# 1. Delete existing app (if needed)
az webapp delete --name $APP_NAME --resource-group $RESOURCE_GROUP

# 2. Create ACR
az acr create \
  --name $ACR_NAME \
  --resource-group $RESOURCE_GROUP \
  --sku Basic \
  --admin-enabled true

# 3. Build and push image
az acr build \
  --registry $ACR_NAME \
  --image pdf-to-tiff:latest \
  --file Dockerfile \
  .

# 4. Get ACR credentials
ACR_USERNAME=$(az acr credential show --name $ACR_NAME --query "username" -o tsv)
ACR_PASSWORD=$(az acr credential show --name $ACR_NAME --query "passwords[0].value" -o tsv)

# 5. Create App Service Plan (if doesn't exist)
az appservice plan create \
  --name $APP_PLAN \
  --resource-group $RESOURCE_GROUP \
  --is-linux \
  --sku B1

# 6. Create Web App with Docker
az webapp create \
  --resource-group $RESOURCE_GROUP \
  --plan $APP_PLAN \
  --name $APP_NAME \
  --deployment-container-image-name $ACR_NAME.azurecr.io/pdf-to-tiff:latest

# 7. Configure container settings
az webapp config container set \
  --name $APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --docker-custom-image-name $ACR_NAME.azurecr.io/pdf-to-tiff:latest \
  --docker-registry-server-url https://$ACR_NAME.azurecr.io \
  --docker-registry-server-user $ACR_USERNAME \
  --docker-registry-server-password $ACR_PASSWORD

# 8. Set application settings
az webapp config appsettings set \
  --name $APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --settings \
    SECRET_KEY="$(openssl rand -hex 32)" \
    WEBSITES_PORT="8000"

# 9. Enable logging
az webapp log config \
  --name $APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --docker-container-logging filesystem

# 10. Restart app
az webapp restart --name $APP_NAME --resource-group $RESOURCE_GROUP

# 11. Check logs
az webapp log tail --name $APP_NAME --resource-group $RESOURCE_GROUP
```

---

## 🔍 Verify Docker Deployment

### Check if you're now using Docker:

```bash
# SSH into container
az webapp ssh --name pdf-to-tiff-app --resource-group pdf-converter-rg

# Once inside, check poppler
which pdfinfo
# Should show: /usr/bin/pdfinfo

pdfinfo -v
# Should show: pdfinfo version 24.02.0

# Exit
exit
```

### Check logs for Docker indicators:

```bash
az webapp log tail --name pdf-to-tiff-app --resource-group pdf-converter-rg
```

Look for:
```
✅ Starting gunicorn 23.0.0
✅ Listening at: http://0.0.0.0:8000
✅ Using worker: sync
```

**NOT**:
```
❌ Oryx 1.0.0
❌ Python 3.13.5
❌ Building with pyproject.toml
```

---

## 🔧 Option 3: Try Oryx Buildpack (Not Recommended)

If you want to keep Python runtime (not Docker), you can try adding an Oryx build script, but **this is less reliable**.

Create `oryx-build.sh`:
```bash
#!/bin/bash
apt-get update
apt-get install -y poppler-utils
```

Then configure in Azure Portal:
- Configuration → Application Settings
- Add: `PRE_BUILD_COMMAND` = `/home/site/wwwroot/oryx-build.sh`

**Problems with this approach:**
- May not work consistently
- Harder to debug
- Less portable

**I strongly recommend Option 1 (Docker) instead.**

---

## 📋 Checklist

After switching to Docker, verify:

- [ ] App is using Docker container (check logs)
- [ ] Poppler is installed (`az webapp ssh` and run `pdfinfo -v`)
- [ ] No more "PDFInfoNotInstalledError" in logs
- [ ] Can upload PDFs successfully
- [ ] Can download TIFF files
- [ ] TIFF files open correctly (not corrupted)
- [ ] All pages from all PDFs are included

---

## 💡 Why Docker is Better

### Current (Python Runtime) ❌:
```
Azure Web App
├─ Oryx builds your Python app
├─ No system package installation
├─ startup.sh runs without sudo
└─ ❌ Poppler can't be installed
```

### Docker Deployment ✅:
```
Azure Web App
└─ Docker Container
    ├─ Built with root access
    ├─ Poppler installed during build
    ├─ Python + all packages
    └─ ✅ Everything works!
```

---

## 🆘 Troubleshooting

### "az: command not found"
Install Azure CLI:
```bash
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash
```

### "not logged in to Azure"
```bash
az login
```

### "ACR name already exists"
The name must be globally unique. Change `ACR_NAME` to something unique like:
```bash
ACR_NAME="pdfconverter$(whoami)$(date +%s)"
```

### "Deployment times out"
The first build takes 5-10 minutes. Be patient. Check logs:
```bash
az webapp log tail --name pdf-to-tiff-app --resource-group pdf-converter-rg
```

### "Container still shows Python runtime in logs"
Make sure you deleted the old app and created a new one with Docker, not just updated settings.

---

## 📞 Next Steps

1. **Choose Option 1 (automated script)** - easiest
2. **Run the deployment** - takes ~10 minutes
3. **Wait for container to start** - takes 2-3 minutes
4. **Test with your PDFs** - should work perfectly now!

---

## Summary

**Current Problem**: You're using Python runtime, not Docker
**Solution**: Switch to Docker deployment with poppler pre-installed
**How**: Run `./deploy_azure.sh` (after editing configuration)
**Time**: ~15 minutes total
**Result**: PDFs will convert successfully! ✅

---

Ready to deploy? Run `./deploy_azure.sh` now! 🚀
