# Azure Docker Deployment - Fix for Poppler Issue

## Problem

Azure Web App **cannot install poppler-utils** using startup.sh because:
- No sudo access in startup scripts
- apt-get requires root privileges
- System packages can't be installed at runtime

**Error**:
```
PDFInfoNotInstalledError: Unable to get page count. Is poppler installed and in PATH?
```

## Solution: Use Docker Deployment

Deploy as a Docker container with poppler pre-installed. This is the **recommended approach** for Azure Web Apps with system dependencies.

---

## Method 1: Deploy via Azure Container Registry (Recommended)

### Step 1: Build and Push Docker Image

```bash
# Login to Azure
az login

# Create resource group (if not exists)
az group create --name pdf-converter-rg --location eastus

# Create Azure Container Registry
az acr create \
  --name pdfconverteracr \
  --resource-group pdf-converter-rg \
  --sku Basic \
  --admin-enabled true

# Login to ACR
az acr login --name pdfconverteracr

# Build and push image
az acr build \
  --registry pdfconverteracr \
  --image pdf-to-tiff:latest \
  --file Dockerfile \
  .
```

### Step 2: Create Web App with Container

```bash
# Create App Service Plan for Linux
az appservice plan create \
  --name pdf-converter-plan \
  --resource-group pdf-converter-rg \
  --is-linux \
  --sku B1

# Get ACR credentials
ACR_USERNAME=$(az acr credential show --name pdfconverteracr --query "username" -o tsv)
ACR_PASSWORD=$(az acr credential show --name pdfconverteracr --query "passwords[0].value" -o tsv)

# Create Web App with container
az webapp create \
  --resource-group pdf-converter-rg \
  --plan pdf-converter-plan \
  --name pdf-to-tiff-app \
  --deployment-container-image-name pdfconverteracr.azurecr.io/pdf-to-tiff:latest

# Configure container registry
az webapp config container set \
  --name pdf-to-tiff-app \
  --resource-group pdf-converter-rg \
  --docker-custom-image-name pdfconverteracr.azurecr.io/pdf-to-tiff:latest \
  --docker-registry-server-url https://pdfconverteracr.azurecr.io \
  --docker-registry-server-user $ACR_USERNAME \
  --docker-registry-server-password $ACR_PASSWORD

# Set SECRET_KEY
az webapp config appsettings set \
  --name pdf-to-tiff-app \
  --resource-group pdf-converter-rg \
  --settings SECRET_KEY="$(openssl rand -hex 32)"

# Enable container logging
az webapp log config \
  --name pdf-to-tiff-app \
  --resource-group pdf-converter-rg \
  --docker-container-logging filesystem
```

### Step 3: Verify Deployment

```bash
# Get app URL
az webapp show \
  --name pdf-to-tiff-app \
  --resource-group pdf-converter-rg \
  --query defaultHostName -o tsv

# Check logs
az webapp log tail \
  --name pdf-to-tiff-app \
  --resource-group pdf-converter-rg
```

---

## Method 2: Deploy via Azure Portal

### Step 1: Build Docker Image Locally

```bash
# Build image
docker build -t pdf-to-tiff:latest .

# Test locally
docker run -p 8000:8000 -e SECRET_KEY="test-key" pdf-to-tiff:latest

# Visit http://localhost:8000 to test
```

### Step 2: Create Azure Container Registry (Portal)

1. Go to [Azure Portal](https://portal.azure.com)
2. Click "+ Create a resource"
3. Search for "Container Registry"
4. Fill in:
   - **Name**: `pdfconverteracr` (must be globally unique)
   - **Resource Group**: Create new or use existing
   - **Location**: Your region
   - **SKU**: Basic
5. Click "Review + Create" → "Create"

### Step 3: Push Image to ACR

```bash
# Login to ACR
az acr login --name pdfconverteracr

# Tag image
docker tag pdf-to-tiff:latest pdfconverteracr.azurecr.io/pdf-to-tiff:latest

# Push image
docker push pdfconverteracr.azurecr.io/pdf-to-tiff:latest
```

### Step 4: Create Web App for Containers (Portal)

1. Go to Azure Portal
2. Click "+ Create a resource" → "Web App"
3. Fill in:
   - **Name**: Your app name
   - **Publish**: **Docker Container**
   - **Operating System**: Linux
   - **Region**: Your region
   - **Plan**: B1 or higher
4. Click "Next: Docker"
5. Configure Docker:
   - **Options**: Single Container
   - **Image Source**: Azure Container Registry
   - **Registry**: pdfconverteracr
   - **Image**: pdf-to-tiff
   - **Tag**: latest
6. Click "Review + Create" → "Create"

### Step 5: Configure App Settings

1. Go to your Web App → Configuration
2. Add Application Setting:
   - **Name**: `SECRET_KEY`
   - **Value**: (generate with `openssl rand -hex 32`)
3. Add Application Setting:
   - **Name**: `WEBSITES_PORT`
   - **Value**: `8000`
4. Click "Save"

---

## Method 3: Docker Compose (Local Development)

```bash
# Build and run
docker-compose up --build

# Visit http://localhost:5000

# Stop
docker-compose down
```

---

## Updating Your Deployment

### After Code Changes

```bash
# Rebuild and push to ACR
az acr build \
  --registry pdfconverteracr \
  --image pdf-to-tiff:latest \
  --file Dockerfile \
  .

# Restart web app to pull latest image
az webapp restart \
  --name pdf-to-tiff-app \
  --resource-group pdf-converter-rg
```

Or with Docker CLI:

```bash
# Build locally
docker build -t pdf-to-tiff:latest .

# Tag for ACR
docker tag pdf-to-tiff:latest pdfconverteracr.azurecr.io/pdf-to-tiff:latest

# Push to ACR
docker push pdfconverteracr.azurecr.io/pdf-to-tiff:latest

# Restart web app
az webapp restart \
  --name pdf-to-tiff-app \
  --resource-group pdf-converter-rg
```

---

## Verification Steps

### 1. Check Container Logs

```bash
az webapp log tail \
  --name pdf-to-tiff-app \
  --resource-group pdf-converter-rg
```

### 2. SSH into Container (if needed)

```bash
az webapp ssh \
  --name pdf-to-tiff-app \
  --resource-group pdf-converter-rg
```

Then verify poppler:
```bash
pdfinfo -v
# Should show: pdfinfo version 24.02.0 or similar
```

### 3. Test the Application

1. Visit your app URL: `https://your-app-name.azurewebsites.net`
2. Upload 2 PDF files
3. Convert to TIFF
4. Download and open the file
5. Verify it's not corrupted

---

## Troubleshooting

### Container won't start

**Check logs:**
```bash
az webapp log tail --name pdf-to-tiff-app --resource-group pdf-converter-rg
```

**Common issues:**
- Port mismatch: Ensure `WEBSITES_PORT` is set to `8000`
- Missing SECRET_KEY: Add in Configuration
- Registry auth: Verify ACR credentials

### "PDFInfoNotInstalledError" still occurs

**Verify poppler in container:**
```bash
# SSH into container
az webapp ssh --name pdf-to-tiff-app --resource-group pdf-converter-rg

# Check poppler
which pdfinfo
pdfinfo -v
```

**If not found, rebuild image:**
```bash
az acr build --registry pdfconverteracr --image pdf-to-tiff:latest --file Dockerfile .
az webapp restart --name pdf-to-tiff-app --resource-group pdf-converter-rg
```

### Container pulls but app doesn't respond

**Check port configuration:**
1. Go to Configuration → Application Settings
2. Add: `WEBSITES_PORT` = `8000`
3. Save and restart

### High memory usage

**Upgrade App Service Plan:**
```bash
az appservice plan update \
  --name pdf-converter-plan \
  --resource-group pdf-converter-rg \
  --sku B2
```

---

## Cost Considerations

### Azure Container Registry
- **Basic**: ~$5/month (sufficient for this app)
- Includes 10GB storage

### App Service Plan
- **B1**: ~$13/month (1.75GB RAM) - Minimum recommended
- **B2**: ~$26/month (3.5GB RAM) - Better for larger files
- **S1**: ~$70/month (1.75GB RAM) - Production with auto-scale

### Total Monthly Cost
- **Development**: ~$18/month (ACR Basic + B1)
- **Production**: ~$31/month (ACR Basic + B2)

---

## Why Docker Deployment?

✅ **Advantages**:
- System dependencies (poppler) pre-installed
- Consistent environment (local = production)
- Easy updates (rebuild and push)
- Better isolation
- Can run on any Azure compute (Web App, Container Instances, AKS)

❌ **Alternative (Not Recommended)**:
- Using Azure Web App with buildpack + startup.sh
- Requires complex oryx build configuration
- Less reliable
- Harder to debug

---

## Quick Reference

### Build and Deploy
```bash
# One-command deploy
az acr build --registry pdfconverteracr --image pdf-to-tiff:latest . && \
az webapp restart --name pdf-to-tiff-app --resource-group pdf-converter-rg
```

### View Logs
```bash
az webapp log tail --name pdf-to-tiff-app --resource-group pdf-converter-rg
```

### Restart App
```bash
az webapp restart --name pdf-to-tiff-app --resource-group pdf-converter-rg
```

### Get App URL
```bash
az webapp show --name pdf-to-tiff-app --resource-group pdf-converter-rg --query defaultHostName -o tsv
```

---

## Summary

1. ✅ Use Docker deployment for Azure
2. ✅ Poppler pre-installed in container
3. ✅ No startup script issues
4. ✅ Consistent environment
5. ✅ Easy updates and rollbacks

**Next Steps**:
1. Choose Method 1 (CLI) or Method 2 (Portal)
2. Build and push Docker image
3. Create Web App with container
4. Configure SECRET_KEY
5. Test with your PDF files

---

For detailed step-by-step, see sections above based on your preferred method.
