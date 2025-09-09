@echo off
REM Oracle Cloud Build and Deploy Script for Windows
REM This script builds the Docker image and prepares for Oracle Cloud deployment

setlocal enabledelayedexpansion

set IMAGE_NAME=phishing-detection-api
set VERSION=%1
if "%VERSION%"=="" set VERSION=latest

set REGION=%OCI_REGION%
if "%REGION%"=="" set REGION=us-ashburn-1

set TENANCY=%OCI_TENANCY%
if "%TENANCY%"=="" set TENANCY=your-tenancy

set NAMESPACE=%OCI_NAMESPACE%
if "%NAMESPACE%"=="" set NAMESPACE=your-namespace

echo.
echo 🚀 Oracle Cloud Deployment Script
echo ==================================

REM Check if Docker is installed
docker --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker is not installed or not in PATH
    exit /b 1
)

echo 📋 Prerequisites check passed

REM Build Docker image
echo.
echo 🔨 Building Docker image...
docker build -t %IMAGE_NAME%:%VERSION% .

if errorlevel 1 (
    echo ❌ Docker build failed
    exit /b 1
)

echo ✅ Docker image built successfully

REM Test image locally
echo.
echo 🧪 Testing image locally...
docker run --rm -d --name test-container -p 8001:8000 -e MONGODB_URI=test -e SECRET_KEY=test-key %IMAGE_NAME%:%VERSION%

timeout /t 10 /nobreak >nul

REM Test health endpoint
curl -f http://localhost:8001/health >nul 2>&1
if errorlevel 1 (
    echo ❌ Local test failed
    docker stop test-container >nul 2>&1
    exit /b 1
) else (
    echo ✅ Local test passed
    docker stop test-container >nul 2>&1
)

REM Tag for Oracle Container Registry
set OCIR_IMAGE=%REGION%.ocir.io/%NAMESPACE%/%IMAGE_NAME%:%VERSION%
echo.
echo 🏷️ Tagging image for OCIR: %OCIR_IMAGE%
docker tag %IMAGE_NAME%:%VERSION% %OCIR_IMAGE%

echo.
echo 🎉 Build completed successfully!
echo.
echo Next steps:
echo 1. Login to OCIR: docker login %REGION%.ocir.io
echo 2. Push image: docker push %OCIR_IMAGE%
echo 3. Create Container Instance in Oracle Cloud Console
echo 4. Use image: %OCIR_IMAGE%
echo 5. Set environment variables from .env file
echo 6. Configure port 8000
echo 7. Allocate at least 1GB memory
echo.
echo Or use Kubernetes deployment:
echo kubectl apply -f oracle-cloud-deploy.yml
echo.
echo 🚀 Happy deploying!

endlocal