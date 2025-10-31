# Quick Start Guide

## Test Locally (5 minutes)

### Option 1: Python directly

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Install poppler (system dependency)
# On Ubuntu/Debian:
sudo apt-get install poppler-utils

# On macOS:
brew install poppler

# 3. Run the app
python app.py

# 4. Open browser to http://localhost:5000
```

### Option 2: Docker

```bash
# Build and run
docker-compose up

# Open browser to http://localhost:5000
```

## Deploy to Azure (15 minutes)

### Prerequisites
- Azure account ([Create free account](https://azure.microsoft.com/free/))
- Git installed

### Steps

1. **Create Azure Web App**
   - Go to [Azure Portal](https://portal.azure.com)
   - Click "+ Create a resource" → "Web App"
   - Fill in:
     - **Name**: `your-app-name` (must be unique)
     - **Runtime**: Python 3.11
     - **Operating System**: Linux
     - **Region**: Choose closest to you
   - Click "Review + Create" → "Create"

2. **Configure App Settings**
   - Go to your Web App → Configuration → Application settings
   - Click "+ New application setting"
   - Add:
     - **Name**: `SECRET_KEY`
     - **Value**: `your-secret-key-here` (generate with `python -c "import secrets; print(secrets.token_hex(32))"`)
   - Click "OK" → "Save"

3. **Set Startup Command**
   - Go to Configuration → General settings
   - Set **Startup Command**: `startup.sh`
   - Click "Save"

4. **Deploy Code**
   - Go to Deployment Center
   - Choose "Local Git" as source
   - Click "Save"
   - Copy the Git Clone URI

5. **Push Code**
   ```bash
   # In your project directory
   git init
   git add .
   git commit -m "Initial commit"

   # Add Azure remote (use your Git Clone URI)
   git remote add azure <your-git-clone-uri>

   # Push to Azure
   git push azure main
   ```

6. **Install System Dependencies**
   - Go to your Web App → SSH (under Development Tools)
   - Run:
   ```bash
   apt-get update
   apt-get install -y poppler-utils
   ```

7. **Access Your App**
   - Visit: `https://your-app-name.azurewebsites.net`
   - Upload PDFs and test!

## Troubleshooting

### Local Testing

**Error: "No module named 'flask'"**
```bash
pip install -r requirements.txt
```

**Error: "pdf2image.exceptions.PDFInfoNotInstalledError"**
```bash
# Install poppler-utils
# Ubuntu: sudo apt-get install poppler-utils
# macOS: brew install poppler
```

### Azure Deployment

**App doesn't start**
- Check logs: Web App → Monitoring → Log stream
- Verify Python version is 3.11
- Check if SECRET_KEY is set

**Conversion fails with "PDFInfoNotInstalled"**
- SSH into app and install poppler:
  ```bash
  apt-get update && apt-get install -y poppler-utils
  ```

**Timeout errors**
- Increase timeout in [startup.sh](startup.sh):
  ```bash
  gunicorn --timeout 600 ...
  ```

## Usage Tips

1. **File Size**: Keep individual PDFs under 50MB
2. **Total Upload**: Maximum 200MB total upload
3. **DPI Settings**:
   - 150 DPI: Good for text documents
   - 200 DPI: Recommended default
   - 300 DPI: High quality scans
   - 400 DPI: Archive quality (large files)
4. **File Order**: Files are processed alphabetically

## Next Steps

- See [README.md](README.md) for detailed documentation
- See [DEPLOYMENT.md](DEPLOYMENT.md) for advanced deployment options
- Consider Docker deployment for easier system dependency management
- Set up custom domain in Azure Portal
- Enable Application Insights for monitoring

## Need Help?

1. Check [DEPLOYMENT.md](DEPLOYMENT.md) troubleshooting section
2. Review Azure Web App logs
3. Test with small files first
4. Verify all dependencies are installed
