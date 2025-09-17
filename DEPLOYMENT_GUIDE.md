# 🚀 AgriSmart NDVI Model - Render Deployment Guide

## Overview
This guide will help you deploy your AgriSmart NDVI model to Render with Google Earth Engine integration in live mode.

## Prerequisites
- ✅ Google Earth Engine account with project access
- ✅ Render account (free tier available)
- ✅ Git repository with your code

## Step 1: Prepare Your Repository

### 1.1 Commit Your Changes
```bash
git add .
git commit -m "Prepare for Render deployment with GEE live mode"
git push origin main
```

### 1.2 Verify Files
Ensure these files are in your repository root:
- `render.yaml` - Render configuration
- `Procfile` - Process configuration
- `requirements-prod.txt` - Production dependencies
- `src/app_prod.py` - Main application
- `src/gee_integration.py` - GEE integration

## Step 2: Set Up Google Earth Engine Authentication

### 2.1 Create Service Account (Recommended for Production)
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Select your project: `crested-primacy-471013-r0`
3. Navigate to **IAM & Admin** > **Service Accounts**
4. Click **Create Service Account**
5. Name: `agrismart-render`
6. Grant roles: **Earth Engine User**
7. Create and download the JSON key file

### 2.2 Alternative: Use Personal Authentication
If you prefer to use your personal GEE account, you can authenticate using the web interface during deployment.

## Step 3: Deploy to Render

### 3.1 Create New Web Service
1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click **New +** > **Web Service**
3. Connect your Git repository
4. Select your repository

### 3.2 Configure Service Settings
- **Name**: `agrismart-api`
- **Environment**: `Python 3`
- **Build Command**: `pip install -r requirements-prod.txt`
- **Start Command**: `gunicorn src.app_prod:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120`
- **Plan**: `Starter` (Free tier)

### 3.3 Set Environment Variables
In the Render dashboard, go to **Environment** tab and add:

```
GEE_MODE=live
GEE_PROJECT=crested-primacy-471013-r0
FLASK_ENV=production
PYTHONPATH=.
```

**For Service Account Authentication (Recommended):**
```
GOOGLE_APPLICATION_CREDENTIALS=/opt/render/project/src/service-account-key.json
```

**For Personal Authentication:**
You'll need to authenticate via the Render shell after deployment.

### 3.4 Deploy
1. Click **Create Web Service**
2. Render will automatically build and deploy your application
3. Monitor the build logs for any issues

## Step 4: Post-Deployment Setup

### 4.1 Authenticate Google Earth Engine
If using personal authentication:

1. Go to your service dashboard
2. Click **Shell** tab
3. Run: `earthengine authenticate`
4. Follow the authentication flow

### 4.2 Test Your Deployment
1. Visit your service URL (e.g., `https://agrismart-api.onrender.com`)
2. Test endpoints:
   - Health: `https://your-app.onrender.com/health`
   - Predict: `https://your-app.onrender.com/predict-gee`
   - Dashboard: `https://your-app.onrender.com/dashboard`

## Step 5: Monitor and Maintain

### 5.1 Health Monitoring
- Use the `/health` endpoint to monitor GEE connection
- Check Render logs for any errors
- Monitor resource usage in Render dashboard

### 5.2 Automatic Deployments
- Render will auto-deploy when you push to your main branch
- Monitor build logs for deployment status

## Troubleshooting

### Common Issues

#### 1. GEE Authentication Failed
```bash
# In Render shell
earthengine authenticate
```

#### 2. Build Failures
- Check `requirements-prod.txt` for version conflicts
- Ensure all dependencies are compatible with Python 3.9+

#### 3. Memory Issues
- Upgrade to a higher Render plan if needed
- Optimize image processing in GEE integration

#### 4. Timeout Errors
- Increase timeout in `render.yaml`
- Optimize GEE queries for faster execution

### Debug Commands
```bash
# Check GEE status
python -c "import ee; print(ee.Initialize())"

# Test GEE integration
python src/gee_integration.py

# Check application health
curl https://your-app.onrender.com/health
```

## Production Considerations

### Security
- Never commit service account keys to Git
- Use Render's environment variables for sensitive data
- Enable HTTPS (automatic with Render)

### Performance
- Monitor memory usage
- Consider upgrading plan for high traffic
- Implement caching for frequent requests

### Monitoring
- Set up alerts for service downtime
- Monitor GEE API quotas
- Track application performance metrics

## API Usage Examples

### Health Check
```bash
curl https://your-app.onrender.com/health
```

### Predict with GEE Data
```bash
curl -X POST https://your-app.onrender.com/predict-gee \
  -H "Content-Type: application/json" \
  -d '{"use_gee": true, "lat": 11.0168, "lon": 76.9558}'
```

### Dashboard
```bash
curl https://your-app.onrender.com/dashboard
```

## Support
- Render Documentation: https://render.com/docs
- Google Earth Engine: https://developers.google.com/earth-engine
- AgriSmart Issues: Check your repository issues

---

🎉 **Congratulations!** Your AgriSmart NDVI model is now deployed and running in production with live Google Earth Engine data!
