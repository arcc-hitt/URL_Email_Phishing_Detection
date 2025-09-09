# Deployment Guide for Oracle Cloud

This guide explains how to deploy the Phishing Detection API on Oracle Cloud Infrastructure (OCI).

## Prerequisites

1. Oracle Cloud account with free tier or paid subscription
2. MongoDB Atlas account (for database)
3. Docker installed locally (for building images)
4. OCI CLI configured (optional but recommended)
5. Your trained ML models in the `app/models/saved/` directory

## Deployment Options

### Option 1: Container Instances (Recommended)

#### Step 1: Prepare Environment Variables

Create a `.env` file in the project root:

```bash
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/phishing_detection_db
SECRET_KEY=your-super-secret-key-here
DEBUG=False
PORT=8000
LOG_LEVEL=INFO
```

#### Step 2: Build Docker Image

```bash
# Build the Docker image
docker build -t phishing-detection-api .

# Test locally
docker-compose up
```

#### Step 3: Push to Oracle Container Registry

```bash
# Tag for Oracle Container Registry
docker tag phishing-detection-api:latest <region>.ocir.io/<tenancy>/phishing-detection-api:latest

# Login to OCIR
docker login <region>.ocir.io

# Push image
docker push <region>.ocir.io/<tenancy>/phishing-detection-api:latest
```

#### Step 4: Create Container Instance

1. Go to Oracle Cloud Console
2. Navigate to "Container Instances"
3. Click "Create Container Instance"
4. Configure:
   - **Name**: phishing-detection-api
   - **Image**: `<region>.ocir.io/<tenancy>/phishing-detection-api:latest`
   - **Shape**: VM.Standard.E2.1.Micro (free tier) or higher
   - **Memory**: 1GB minimum, 2GB recommended
   - **Environment Variables**: Add your `.env` variables
   - **Port**: 8000

### Option 2: Compute Instance with Docker

#### Step 1: Create Compute Instance

1. Create VM.Standard.E2.1.Micro instance (free tier eligible)
2. Choose Ubuntu 20.04 or later
3. Configure security list to allow port 8000

#### Step 2: Setup Instance

```bash
# Connect to instance
ssh -i your-key.pem ubuntu@<instance-ip>

# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
sudo apt install docker.io docker-compose -y
sudo usermod -aG docker ubuntu

# Clone your repository
git clone <your-repo-url>
cd phishing-detection-backend
```

#### Step 3: Deploy Application

```bash
# Create .env file with your variables
nano .env

# Build and run
docker-compose up -d

# Check logs
docker-compose logs -f
```

### Option 3: Oracle Kubernetes Engine (OKE)

Use the provided `oracle-cloud-deploy.yml` for Kubernetes deployment:

```bash
# Apply configuration
kubectl apply -f oracle-cloud-deploy.yml

# Create secrets
kubectl create secret generic phishing-api-secrets \
  --from-literal=mongodb-uri="your-mongodb-uri" \
  --from-literal=secret-key="your-secret-key"
```

## API Endpoints

- `GET /health` - General health check
- `GET /api/url/health` - URL analysis service health check
- `POST /api/url/analyze` - Analyze URL for phishing
- `GET /api/phishing-logs` - Get phishing detection logs

## Troubleshooting

### Common Issues:

1. **Import Errors**: Make sure all dependencies are installed in the virtual environment
2. **Model Loading Errors**: Ensure model files are in `app/models/saved/`
3. **MongoDB Connection**: Check your MongoDB URI and network access
4. **Memory Issues**: Use only 1 Gunicorn worker for PythonAnywhere free tier

### Logs

Check the error logs in PythonAnywhere:
- Web app error log
- Server log

### Performance Tips

1. Use only 1 worker process to conserve memory
2. Set appropriate timeouts for model loading
3. Monitor memory usage in PythonAnywhere dashboard

## Environment Variables Reference

| Variable | Description | Default |
|----------|-------------|---------|
| `MONGODB_URI` | MongoDB connection string | Required |
| `SECRET_KEY` | Flask secret key | Required |
| `DEBUG` | Enable debug mode | False |
| `PORT` | Server port | 5000 |
| `LOG_LEVEL` | Logging level | INFO |

## Security Notes

1. Never commit `.env` file to version control
2. Use strong secret keys
3. Keep MongoDB credentials secure
4. Regularly update dependencies

## Support

If you encounter issues:
1. Check the startup test results
2. Review PythonAnywhere error logs
3. Verify all environment variables are set
4. Ensure model files are present and accessible
## Step 
4: Configure Load Balancer (Optional)

For production deployments, configure Oracle Cloud Load Balancer:

1. Create Load Balancer in OCI Console
2. Configure backend set with your container instances
3. Set health check to `/health` endpoint
4. Configure SSL certificate if needed

## Step 5: Test Deployment

Test the deployed endpoints:

```bash
# Health check
curl http://<your-instance-ip>:8000/health

# URL analysis health check
curl http://<your-instance-ip>:8000/api/url/health

# Test URL analysis
curl -X POST http://<your-instance-ip>:8000/api/url/analyze \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com"}'
```

## API Endpoints

- `GET /health` - General health check
- `GET /api/url/health` - URL analysis service health check
- `POST /api/url/analyze` - Analyze URL for phishing
- `GET /api/phishing-logs` - Get phishing detection logs

## Monitoring and Logging

### Oracle Cloud Monitoring

1. Enable monitoring for your container instances
2. Set up alerts for:
   - High memory usage (>80%)
   - High CPU usage (>80%)
   - Application errors
   - Health check failures

### Application Logs

```bash
# View container logs
docker logs <container-id>

# Follow logs in real-time
docker logs -f <container-id>

# For Kubernetes
kubectl logs -f deployment/phishing-detection-api
```

## Scaling

### Horizontal Scaling

For high traffic, scale horizontally:

```bash
# Scale Kubernetes deployment
kubectl scale deployment phishing-detection-api --replicas=3

# For container instances, create multiple instances behind load balancer
```

### Vertical Scaling

Upgrade to larger compute shapes:
- VM.Standard.E2.2 (2 OCPUs, 16GB RAM)
- VM.Standard.E2.4 (4 OCPUs, 32GB RAM)

## Troubleshooting

### Common Issues:

1. **Container fails to start**
   - Check environment variables
   - Verify model files are included in image
   - Check memory allocation (minimum 1GB)

2. **Model loading errors**
   - Ensure model files are in correct path
   - Check file permissions
   - Verify TensorFlow compatibility

3. **MongoDB connection issues**
   - Verify MongoDB URI format
   - Check network connectivity
   - Ensure MongoDB Atlas allows Oracle Cloud IPs

4. **Memory issues**
   - Increase container memory allocation
   - Use single worker process if needed
   - Monitor memory usage with Oracle Cloud Monitoring

### Performance Optimization

1. **Use Oracle Cloud CDN** for static assets
2. **Enable caching** for frequent requests
3. **Use Oracle Autonomous Database** for better performance
4. **Implement connection pooling** for MongoDB

## Security Best Practices

1. **Use Oracle Cloud Vault** for secrets management
2. **Enable WAF** (Web Application Firewall)
3. **Configure security lists** to restrict access
4. **Use private subnets** for backend services
5. **Enable audit logging**
6. **Regular security updates** for base images

## Cost Optimization

1. **Use Always Free resources** when possible
2. **Auto-scaling** to handle variable load
3. **Scheduled scaling** for predictable patterns
4. **Resource monitoring** to optimize allocation

## Backup and Disaster Recovery

1. **Database backups** via MongoDB Atlas
2. **Container image backups** in OCIR
3. **Configuration backups** in version control
4. **Multi-region deployment** for high availability

## Environment Variables Reference

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `MONGODB_URI` | MongoDB connection string | - | Yes |
| `SECRET_KEY` | Flask secret key | - | Yes |
| `DEBUG` | Enable debug mode | False | No |
| `PORT` | Server port | 8000 | No |
| `LOG_LEVEL` | Logging level | INFO | No |

## Oracle Cloud Free Tier Limits

- **Compute**: 2 VM.Standard.E2.1.Micro instances
- **Storage**: 200GB total
- **Network**: 10TB outbound per month
- **Load Balancer**: 1 load balancer (10 Mbps)

## Support and Maintenance

1. **Monitor application health** regularly
2. **Update dependencies** monthly
3. **Review logs** for errors and performance issues
4. **Test disaster recovery** procedures
5. **Keep documentation** updated

For issues specific to Oracle Cloud, consult the [Oracle Cloud Documentation](https://docs.oracle.com/en-us/iaas/) or contact Oracle Support.