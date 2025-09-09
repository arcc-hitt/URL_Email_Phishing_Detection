# Oracle Cloud Quick Start Guide

Get your Phishing Detection API running on Oracle Cloud in minutes!

## 🚀 Quick Deploy (Container Instance)

### 1. Prerequisites
- Oracle Cloud account (free tier works!)
- MongoDB Atlas database
- Docker installed locally

### 2. Prepare Environment
```bash
# Clone and navigate to project
cd phishing-detection-backend

# Copy environment template
cp .env.oracle-cloud .env

# Edit .env with your MongoDB URI and secret key
nano .env
```

### 3. Build and Test Locally
```bash
# Windows
build-and-deploy.bat

# Linux/Mac
chmod +x build-and-deploy.sh
./build-and-deploy.sh
```

### 4. Deploy to Oracle Cloud

#### Option A: Container Instance (Easiest)
1. Go to [Oracle Cloud Console](https://cloud.oracle.com)
2. Navigate to **Container Instances**
3. Click **Create Container Instance**
4. Fill in:
   - **Name**: `phishing-detection-api`
   - **Image**: Use the image from step 3
   - **Shape**: `VM.Standard.E2.1.Micro` (free tier)
   - **Memory**: 1GB minimum
   - **Port**: 8000
   - **Environment Variables**: Copy from your `.env` file

#### Option B: Compute Instance
1. Create **VM.Standard.E2.1.Micro** instance
2. SSH into instance:
   ```bash
   ssh -i your-key.pem ubuntu@<instance-ip>
   ```
3. Install Docker:
   ```bash
   sudo apt update
   sudo apt install docker.io docker-compose -y
   sudo usermod -aG docker ubuntu
   ```
4. Deploy:
   ```bash
   git clone <your-repo>
   cd phishing-detection-backend
   # Create .env file
   docker-compose up -d
   ```

### 5. Test Your Deployment
```bash
# Replace with your instance IP
curl http://<your-ip>:8000/health

# Test URL analysis
curl -X POST http://<your-ip>:8000/api/url/analyze \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com"}'
```

## 🔧 Configuration

### Environment Variables
| Variable | Description | Required |
|----------|-------------|----------|
| `MONGODB_URI` | MongoDB connection string | ✅ |
| `SECRET_KEY` | Flask secret key | ✅ |
| `DEBUG` | Debug mode (False for production) | ❌ |
| `PORT` | Application port (default: 8000) | ❌ |
| `LOG_LEVEL` | Logging level (INFO, DEBUG, ERROR) | ❌ |

### MongoDB Setup
1. Create free MongoDB Atlas cluster
2. Add Oracle Cloud IPs to whitelist (or use 0.0.0.0/0 for testing)
3. Create database user
4. Get connection string

## 📊 Monitoring

### Health Checks
- **General**: `GET /health`
- **Service**: `GET /api/url/health`

### Logs
```bash
# Container Instance logs via OCI Console
# Or for Compute Instance:
docker logs -f <container-name>
```

## 🔒 Security

### Production Checklist
- [ ] Change default SECRET_KEY
- [ ] Use strong MongoDB credentials
- [ ] Configure Oracle Cloud Security Lists
- [ ] Enable HTTPS with Load Balancer
- [ ] Regular security updates

### Network Security
1. Create Security List allowing port 8000
2. Configure Load Balancer for HTTPS
3. Use private subnets for backend services

## 💰 Cost Optimization

### Free Tier Resources
- **2x VM.Standard.E2.1.Micro** instances (always free)
- **200GB** total storage
- **10TB** outbound data transfer/month
- **1x Load Balancer** (10 Mbps)

### Tips
- Use single instance for development
- Scale horizontally for production
- Monitor usage in OCI Console
- Set up billing alerts

## 🆘 Troubleshooting

### Common Issues

**Container won't start**
```bash
# Check logs
docker logs <container-id>

# Verify environment variables
docker exec -it <container-id> env
```

**Memory issues**
- Increase container memory to 2GB
- Use single worker process
- Monitor with `docker stats`

**Network connectivity**
- Check Security Lists
- Verify port 8000 is open
- Test with `telnet <ip> 8000`

**Model loading errors**
- Ensure model files are in image
- Check file permissions
- Verify sufficient memory

### Getting Help
1. Check Oracle Cloud documentation
2. Review application logs
3. Test with health check endpoints
4. Contact Oracle Cloud support

## 🎯 Next Steps

1. **Set up monitoring** with Oracle Cloud Monitoring
2. **Configure alerts** for high resource usage
3. **Implement CI/CD** with Oracle Cloud DevOps
4. **Add caching** with Oracle Cloud Redis
5. **Scale horizontally** with multiple instances

## 📚 Additional Resources

- [Oracle Cloud Free Tier](https://www.oracle.com/cloud/free/)
- [Container Instances Documentation](https://docs.oracle.com/en-us/iaas/Content/container-instances/home.htm)
- [MongoDB Atlas](https://www.mongodb.com/atlas)
- [Docker Documentation](https://docs.docker.com/)

---

🎉 **Congratulations!** Your Phishing Detection API is now running on Oracle Cloud!