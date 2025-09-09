#!/bin/bash

# Oracle Cloud Build and Deploy Script
# This script builds the Docker image and deploys to Oracle Cloud

set -e

# Configuration
IMAGE_NAME="phishing-detection-api"
VERSION=${1:-latest}
REGION=${OCI_REGION:-"us-ashburn-1"}
TENANCY=${OCI_TENANCY}
NAMESPACE=${OCI_NAMESPACE}

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}🚀 Oracle Cloud Deployment Script${NC}"
echo "=================================="

# Check prerequisites
echo -e "${YELLOW}📋 Checking prerequisites...${NC}"

if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Docker is not installed${NC}"
    exit 1
fi

if ! command -v oci &> /dev/null; then
    echo -e "${YELLOW}⚠️  OCI CLI not found. Manual deployment required.${NC}"
fi

if [ -z "$TENANCY" ]; then
    echo -e "${YELLOW}⚠️  OCI_TENANCY not set. Using default.${NC}"
    TENANCY="your-tenancy"
fi

if [ -z "$NAMESPACE" ]; then
    echo -e "${YELLOW}⚠️  OCI_NAMESPACE not set. Using default.${NC}"
    NAMESPACE="your-namespace"
fi

# Build Docker image
echo -e "${YELLOW}🔨 Building Docker image...${NC}"
docker build -t ${IMAGE_NAME}:${VERSION} .

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Docker image built successfully${NC}"
else
    echo -e "${RED}❌ Docker build failed${NC}"
    exit 1
fi

# Test image locally
echo -e "${YELLOW}🧪 Testing image locally...${NC}"
docker run --rm -d --name test-container -p 8001:8000 \
    -e MONGODB_URI="test" \
    -e SECRET_KEY="test-key" \
    ${IMAGE_NAME}:${VERSION}

sleep 10

# Test health endpoint
if curl -f http://localhost:8001/health > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Local test passed${NC}"
    docker stop test-container
else
    echo -e "${RED}❌ Local test failed${NC}"
    docker stop test-container
    exit 1
fi

# Tag for Oracle Container Registry
OCIR_IMAGE="${REGION}.ocir.io/${NAMESPACE}/${IMAGE_NAME}:${VERSION}"
echo -e "${YELLOW}🏷️  Tagging image for OCIR: ${OCIR_IMAGE}${NC}"
docker tag ${IMAGE_NAME}:${VERSION} ${OCIR_IMAGE}

# Push to OCIR (if OCI CLI is available)
if command -v oci &> /dev/null; then
    echo -e "${YELLOW}📤 Pushing to Oracle Container Registry...${NC}"
    
    # Login to OCIR
    echo "Logging into OCIR..."
    docker login ${REGION}.ocir.io
    
    # Push image
    docker push ${OCIR_IMAGE}
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ Image pushed to OCIR successfully${NC}"
    else
        echo -e "${RED}❌ Failed to push to OCIR${NC}"
        exit 1
    fi
else
    echo -e "${YELLOW}⚠️  OCI CLI not available. Manual push required:${NC}"
    echo "docker login ${REGION}.ocir.io"
    echo "docker push ${OCIR_IMAGE}"
fi

# Deployment instructions
echo -e "${GREEN}🎉 Build completed successfully!${NC}"
echo ""
echo "Next steps:"
echo "1. Create Container Instance in Oracle Cloud Console"
echo "2. Use image: ${OCIR_IMAGE}"
echo "3. Set environment variables from .env file"
echo "4. Configure port 8000"
echo "5. Allocate at least 1GB memory"
echo ""
echo "Or use Kubernetes deployment:"
echo "kubectl apply -f oracle-cloud-deploy.yml"
echo ""
echo -e "${GREEN}🚀 Happy deploying!${NC}"