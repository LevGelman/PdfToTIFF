# Deployment Guide for Azure Web App

This guide explains how to deploy the PDF to TIFF Converter Flask application to Azure Web App.

## Prerequisites

1. Azure account with an active subscription
2. Azure CLI installed (optional, for command line deployment)
3. Git installed on your machine

## Method 1: Deploy via Azure Portal (Recommended for beginners)

### Step 1: Create Azure Web App

1. Go to [Azure Portal](https://portal.azure.com)
2. Click "Create a resource" → "Web App"
3. Configure the web app:
   - **Resource Group**: Create new or select existing
   - **Name**: Choose a unique name (e.g., `pdf-to-tiff-converter`)
   - **Publish**: Code
   - **Runtime stack**: Python 3.11 (or latest available)
   - **Operating System**: Linux
   - **Region**: Choose closest to your users
   - **Pricing Plan**: Free F1 or Basic B1 (F1 has limitations)

4. Click "Review + Create" → "Create"

### Step 2: Configure Application Settings

1. Go to your Web App → **Configuration** → **Application settings**
2. Add new application setting:
   - **Name**: `SECRET_KEY`
   - **Value**: Generate a random string (e.g., using `python -c "import secrets; print(secrets.token_hex(32))"`)
3. Click "Save"

### Step 3: Configure Startup Command

1. Go to **Configuration** → **General settings**
2. Set **Startup Command**: `startup.sh`
3. Click "Save"

### Step 4: Deploy from Local Git

1. Go to **Deployment Center**
2. Select **Source**: Local Git
3. Click "Save"
4. Note the Git Clone URI (e.g., `https://username@yourapp.scm.azurewebsites.net/yourapp.git`)

### Step 5: Deploy Your Code

In your local project directory:

```bash
# Initialize git repository (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit - PDF to TIFF converter"

# Add Azure remote (replace with your Git Clone URI)
git remote add azure https://username@yourapp.scm.azurewebsites.net/yourapp.git

# Push to Azure
git push azure main
```

You'll be prompted for deployment credentials (found in **Deployment Center** → **FTPS credentials**)

### Step 6: Install System Dependencies

Since the app requires `poppler-utils`, you need to install it:

1. Go to **Development Tools** → **SSH** or **Console**
2. Run:
```bash
apt-get update
apt-get install -y poppler-utils
```

**Note**: System packages need to be reinstalled after each deployment or app restart. For persistent installation, use a Docker container deployment instead.

### Step 7: Test Your Application

1. Go to your app URL: `https://your-app-name.azurewebsites.net`
2. Upload PDF files and test the conversion

## Method 2: Deploy via Azure CLI

### Install Azure CLI

```bash
# macOS
brew install azure-cli

# Windows
# Download from: https://aka.ms/installazurecliwindows

# Linux
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash
```

### Deploy Commands

```bash
# Login to Azure
az login

# Create resource group
az group create --name pdf-converter-rg --location eastus

# Create App Service plan
az appservice plan create \
  --name pdf-converter-plan \
  --resource-group pdf-converter-rg \
  --sku B1 \
  --is-linux

# Create web app
az webapp create \
  --name pdf-to-tiff-converter \
  --resource-group pdf-converter-rg \
  --plan pdf-converter-plan \
  --runtime "PYTHON:3.11"

# Configure startup command
az webapp config set \
  --name pdf-to-tiff-converter \
  --resource-group pdf-converter-rg \
  --startup-file "startup.sh"

# Set secret key
az webapp config appsettings set \
  --name pdf-to-tiff-converter \
  --resource-group pdf-converter-rg \
  --settings SECRET_KEY="your-secret-key-here"

# Deploy from local git
az webapp deployment source config-local-git \
  --name pdf-to-tiff-converter \
  --resource-group pdf-converter-rg

# Get deployment credentials
az webapp deployment list-publishing-credentials \
  --name pdf-to-tiff-converter \
  --resource-group pdf-converter-rg

# Deploy code
git remote add azure <git-url-from-previous-command>
git push azure main
```

## Method 3: Deploy with Docker (Recommended for Production)

Create a `Dockerfile`:

```dockerfile
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && \
    apt-get install -y poppler-utils && \
    rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create temp directory
RUN mkdir -p /tmp

# Set environment variables
ENV FLASK_APP=app.py
ENV PORT=8000

# Expose port
EXPOSE 8000

# Run the application
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--timeout", "600", "--workers", "2", "app:app"]
```

Deploy to Azure Container Registry and Web App for Containers:

```bash
# Create container registry
az acr create \
  --name pdfconverterregistry \
  --resource-group pdf-converter-rg \
  --sku Basic \
  --admin-enabled true

# Build and push image
az acr build \
  --registry pdfconverterregistry \
  --image pdf-to-tiff:latest \
  .

# Create web app with container
az webapp create \
  --name pdf-to-tiff-converter \
  --resource-group pdf-converter-rg \
  --plan pdf-converter-plan \
  --deployment-container-image-name pdfconverterregistry.azurecr.io/pdf-to-tiff:latest
```

## Local Testing

Before deploying, test locally:

```bash
# Install dependencies
pip install -r requirements.txt

# Install poppler (system dependency)
# Ubuntu/Debian:
sudo apt-get install poppler-utils

# macOS:
brew install poppler

# Run the application
python app.py

# Visit http://localhost:5000
```

## Configuration Options

### Environment Variables

Set these in Azure Portal → Configuration → Application settings:

- `SECRET_KEY`: Secret key for Flask sessions (required)
- `PORT`: Port number (default: 8000)
- `FLASK_ENV`: Set to `production` for production

### File Upload Limits

Current limits in `app.py`:
- Maximum file size per file: 50MB
- Maximum total upload: 200MB

To change, edit these lines in `app.py`:
```python
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB per file
app.config['MAX_CONTENT_LENGTH'] = 200 * 1024 * 1024  # 200MB total
```

### Timeout Settings

For large files, increase timeout in `startup.sh`:
```bash
gunicorn --bind=0.0.0.0:8000 --timeout 600 --workers=2 app:app
```

## Troubleshooting

### Application doesn't start

1. Check logs in Azure Portal → **Monitoring** → **Log stream**
2. Verify Python version matches runtime stack
3. Check if `poppler-utils` is installed

### "pdf2image.exceptions.PDFInfoNotInstalledError"

Install poppler-utils via SSH/Console:
```bash
apt-get update && apt-get install -y poppler-utils
```

### Timeout errors during conversion

1. Increase timeout in `startup.sh`
2. Consider upgrading to higher tier App Service plan
3. Reduce DPI or file sizes

### Out of memory errors

1. Upgrade to App Service plan with more memory
2. Reduce number of Gunicorn workers
3. Process fewer files simultaneously

## Monitoring and Logs

### View Application Logs

1. Go to **Monitoring** → **Log stream**
2. Or download logs: **Monitoring** → **App Service logs** → Enable **Application logging**

### View Metrics

Go to **Monitoring** → **Metrics** to see:
- Response time
- Request count
- Memory usage
- CPU usage

## Security Best Practices

1. ✅ Use HTTPS (enabled by default on Azure)
2. ✅ Set strong `SECRET_KEY`
3. ✅ File type validation (only PDFs allowed)
4. ✅ File size limits enforced
5. ✅ Use temporary files that auto-cleanup
6. ⚠️ Consider adding authentication for production use
7. ⚠️ Consider rate limiting for public deployments

## Cost Optimization

### Free Tier (F1)
- Free for 60 CPU minutes/day
- Good for testing
- Limited memory (1GB)

### Basic Tier (B1)
- ~$13/month
- Better for production
- More memory and CPU

### Tips to reduce costs:
1. Stop app when not in use (in Azure Portal)
2. Use auto-scaling based on demand
3. Monitor usage in **Cost Management**

## Updating the Application

```bash
# Make changes to code
git add .
git commit -m "Update: description of changes"

# Push to Azure
git push azure main

# Azure will automatically redeploy
```

## Backup and Restore

1. Go to **Backups** in Azure Portal
2. Configure automated backups
3. Include configuration in backup

## Support and Resources

- [Azure Web Apps Documentation](https://docs.microsoft.com/azure/app-service/)
- [Flask Deployment Guide](https://flask.palletsprojects.com/en/latest/deploying/)
- [Azure Python Developer Center](https://docs.microsoft.com/azure/developer/python/)

## Quick Checklist

- [ ] Create Azure Web App (Python 3.11, Linux)
- [ ] Set SECRET_KEY in Application Settings
- [ ] Configure startup command: `startup.sh`
- [ ] Deploy code via Git
- [ ] Install poppler-utils via SSH
- [ ] Test application at your Azure URL
- [ ] Monitor logs for any errors
- [ ] Set up backups (optional)
- [ ] Configure custom domain (optional)
