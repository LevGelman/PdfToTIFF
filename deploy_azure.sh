#!/bin/bash

# Quick Azure Docker Deployment Script
# This script automates the Docker deployment to Azure

set -e  # Exit on error

echo "=================================================="
echo "PDF to TIFF Converter - Azure Docker Deployment"
echo "=================================================="
echo

# Configuration - CHANGE THESE VALUES
ACR_NAME="pdfconverteracr"              # Your ACR name (must be globally unique)
RESOURCE_GROUP="pdf-converter-rg"       # Your resource group name
APP_NAME="pdf-to-tiff-app"             # Your web app name
LOCATION="eastus"                       # Azure region
APP_PLAN="pdf-converter-plan"          # App Service Plan name

echo "Configuration:"
echo "  ACR Name: $ACR_NAME"
echo "  Resource Group: $RESOURCE_GROUP"
echo "  App Name: $APP_NAME"
echo "  Location: $LOCATION"
echo

# Check if Azure CLI is installed
if ! command -v az &> /dev/null; then
    echo "❌ Azure CLI is not installed."
    echo "Install from: https://aka.ms/InstallAzureCLIDeb"
    exit 1
fi

echo "✓ Azure CLI found"

# Check if logged in
echo
echo "Checking Azure login status..."
if ! az account show &> /dev/null; then
    echo "❌ Not logged into Azure. Running 'az login'..."
    az login
else
    echo "✓ Already logged into Azure"
    az account show --query "{Subscription:name, User:user.name}" -o table
fi

# Ask user to continue
echo
read -p "Continue with deployment? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Deployment cancelled."
    exit 0
fi

# Create resource group
echo
echo "Creating resource group..."
if az group show --name $RESOURCE_GROUP &> /dev/null; then
    echo "✓ Resource group '$RESOURCE_GROUP' already exists"
else
    az group create --name $RESOURCE_GROUP --location $LOCATION
    echo "✓ Resource group created"
fi

# Create Azure Container Registry
echo
echo "Creating Azure Container Registry..."
if az acr show --name $ACR_NAME &> /dev/null; then
    echo "✓ ACR '$ACR_NAME' already exists"
else
    az acr create \
      --name $ACR_NAME \
      --resource-group $RESOURCE_GROUP \
      --sku Basic \
      --admin-enabled true
    echo "✓ ACR created"
fi

# Build and push image to ACR
echo
echo "Building and pushing Docker image to ACR..."
echo "This may take 3-5 minutes..."
az acr build \
  --registry $ACR_NAME \
  --image pdf-to-tiff:latest \
  --file Dockerfile \
  .
echo "✓ Image built and pushed"

# Create App Service Plan
echo
echo "Creating App Service Plan..."
if az appservice plan show --name $APP_PLAN --resource-group $RESOURCE_GROUP &> /dev/null; then
    echo "✓ App Service Plan '$APP_PLAN' already exists"
else
    az appservice plan create \
      --name $APP_PLAN \
      --resource-group $RESOURCE_GROUP \
      --is-linux \
      --sku B1
    echo "✓ App Service Plan created"
fi

# Get ACR credentials
echo
echo "Getting ACR credentials..."
ACR_USERNAME=$(az acr credential show --name $ACR_NAME --query "username" -o tsv)
ACR_PASSWORD=$(az acr credential show --name $ACR_NAME --query "passwords[0].value" -o tsv)
echo "✓ Credentials retrieved"

# Create or update Web App
echo
echo "Creating/updating Web App..."
if az webapp show --name $APP_NAME --resource-group $RESOURCE_GROUP &> /dev/null; then
    echo "✓ Web App '$APP_NAME' already exists - updating..."

    # Update container settings
    az webapp config container set \
      --name $APP_NAME \
      --resource-group $RESOURCE_GROUP \
      --docker-custom-image-name $ACR_NAME.azurecr.io/pdf-to-tiff:latest \
      --docker-registry-server-url https://$ACR_NAME.azurecr.io \
      --docker-registry-server-user $ACR_USERNAME \
      --docker-registry-server-password $ACR_PASSWORD
else
    # Create new web app
    az webapp create \
      --resource-group $RESOURCE_GROUP \
      --plan $APP_PLAN \
      --name $APP_NAME \
      --deployment-container-image-name $ACR_NAME.azurecr.io/pdf-to-tiff:latest

    # Configure container
    az webapp config container set \
      --name $APP_NAME \
      --resource-group $RESOURCE_GROUP \
      --docker-custom-image-name $ACR_NAME.azurecr.io/pdf-to-tiff:latest \
      --docker-registry-server-url https://$ACR_NAME.azurecr.io \
      --docker-registry-server-user $ACR_USERNAME \
      --docker-registry-server-password $ACR_PASSWORD
fi

echo "✓ Web App configured"

# Generate SECRET_KEY if not exists
echo
echo "Configuring application settings..."
SECRET_KEY=$(openssl rand -hex 32)
az webapp config appsettings set \
  --name $APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --settings \
    SECRET_KEY="$SECRET_KEY" \
    WEBSITES_PORT="8000" \
    --output none

echo "✓ Application settings configured"

# Enable container logging
echo
echo "Enabling container logging..."
az webapp log config \
  --name $APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --docker-container-logging filesystem \
  --output none

echo "✓ Logging enabled"

# Restart web app
echo
echo "Restarting web app..."
az webapp restart \
  --name $APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --output none

echo "✓ Web app restarted"

# Get app URL
echo
echo "=================================================="
echo "Deployment Complete!"
echo "=================================================="
echo
APP_URL="https://$(az webapp show --name $APP_NAME --resource-group $RESOURCE_GROUP --query defaultHostName -o tsv)"
echo "Your app is available at:"
echo "  $APP_URL"
echo
echo "It may take 2-3 minutes for the container to start."
echo
echo "To view logs:"
echo "  az webapp log tail --name $APP_NAME --resource-group $RESOURCE_GROUP"
echo
echo "To update after code changes:"
echo "  az acr build --registry $ACR_NAME --image pdf-to-tiff:latest ."
echo "  az webapp restart --name $APP_NAME --resource-group $RESOURCE_GROUP"
echo
echo "=================================================="
