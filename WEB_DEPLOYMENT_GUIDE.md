# Gear Engine - Deployment Guide

Complete instructions for deploying the Gear Engine web application to GitHub Pages and cloud platforms.

## Table of Contents
1. [Frontend Deployment (GitHub Pages)](#frontend-deployment-github-pages)
2. [Backend Deployment Options](#backend-deployment-options)
3. [Development Setup](#development-setup)
4. [Production Deployment](#production-deployment)
5. [Environment Configuration](#environment-configuration)
6. [Troubleshooting](#troubleshooting)

---

## Frontend Deployment (GitHub Pages)

### Prerequisites
- GitHub account
- Git installed locally
- Repository with this project

### Step 1: Prepare Repository Structure

```bash
# Clone or navigate to your gear_engine repository
cd gear_engine

# Ensure you have the following structure:
# gear_engine/
# ├── index.html
# ├── styles/
# │   ├── main.css
# │   └── responsive.css
# ├── js/
# │   ├── api-client.js
# │   ├── 3d-viewer.js
# │   ├── form-manager.js
# │   ├── main.js
# │   └── three.min.js
# └── ...other files
```

### Step 2: Update Three.js Library

The application requires Three.js. You have two options:

**Option A: CDN (Recommended for GitHub Pages)**
Edit `index.html` and replace:
```html
<script src="js/three.min.js"></script>
```
With:
```html
<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
```

**Option B: Local File**
Download Three.js from https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js
Save to `js/three.min.js`

### Step 3: Update API Configuration

Edit `js/main.js` and update the API endpoint. For GitHub Pages, you'll need a separate backend:

```javascript
// Option 1: Use a remote API server
apiClient.setBaseUrl('https://your-api-server.com/api');

// Option 2: Environment-specific configuration
const isProduction = window.location.hostname !== 'localhost';
const apiUrl = isProduction 
    ? 'https://your-api-server.com/api'
    : 'http://localhost:3000/api';
apiClient.setBaseUrl(apiUrl);
```

### Step 4: Configure GitHub Pages

1. Go to your GitHub repository settings
2. Navigate to "Pages" section
3. Set "Source" to "Deploy from a branch"
4. Select "main" (or your default branch) and "/" (root)
5. Click "Save"

Your site will be available at: `https://yourusername.github.io/gear_engine/`

### Step 5: Update Links and URLs

Update any hardcoded URLs in the application:

**In `index.html`:**
```html
<!-- Update links in footer and about section -->
<a href="https://github.com/yourusername/gear_engine" target="_blank">
```

**In `js/api-client.js`:**
```javascript
constructor(baseUrl = 'https://your-api-server.com/api') {
    // ...
}
```

### Step 6: Deploy Frontend

```bash
# Commit and push to GitHub
git add .
git commit -m "Deploy Gear Engine web interface"
git push origin main
```

GitHub Pages will automatically build and deploy your site. Check the "Actions" tab to see deployment status.

---

## Backend Deployment Options

The backend can be deployed on several platforms. Choose one based on your needs:

### Option 1: Railway (Recommended for Beginners)

Railway is easy to set up and offers free tier hosting.

**Steps:**
1. Go to https://railway.app
2. Click "Create New Project"
3. Choose "Deploy from GitHub repo"
4. Select your gear_engine repository
5. Add environment variables:
   ```
   PYTHON_API_URL=http://localhost:8000
   NODE_ENV=production
   PORT=3000
   ```
6. Deploy

Your API will be available at: `https://your-app-name.up.railway.app/api/`

### Option 2: Heroku

```bash
# Install Heroku CLI
# Login to Heroku
heroku login

# Create Heroku app
heroku create gear-engine-api

# Set environment variables
heroku config:set PYTHON_API_URL=http://localhost:8000

# Deploy
git push heroku main

# View logs
heroku logs --tail
```

Your API will be available at: `https://gear-engine-api.herokuapp.com/api/`

### Option 3: Vercel (Serverless)

```bash
# Install Vercel CLI
npm install -g vercel

# Deploy
vercel

# Set environment variables via Vercel dashboard
# Add: PYTHON_API_URL=http://localhost:8000
```

### Option 4: Docker (Any Cloud Provider)

**Build Docker image:**
```bash
docker build -f Dockerfile.backend -t gear-engine-api .
```

**Run locally:**
```bash
docker run -p 3000:3000 -e PYTHON_API_URL=http://python-backend:8000 gear-engine-api
```

**Deploy to cloud (AWS, Google Cloud, DigitalOcean, etc.):**
Follow your cloud provider's documentation for Docker deployment.

### Option 5: Python Backend with FastAPI

If you want to run the Python backend directly:

```bash
# Install dependencies
pip install -r requirements.txt

# Run the server
python -m interfaces.fastapi_app

# The API will be available at http://localhost:8000
```

Then point your Node.js server to this URL:
```
PYTHON_API_URL=http://localhost:8000
```

---

## Development Setup

### Local Development

```bash
# Install Node.js dependencies
npm install

# Start the development server
npm run dev

# In another terminal, start Python backend (if available)
cd path/to/python/backend
python -m interfaces.fastapi_app
```

The application will be available at: `http://localhost:3000`

### Environment Variables

Create a `.env` file:
```env
PORT=3000
NODE_ENV=development
PYTHON_API_URL=http://localhost:8000
```

### Testing

```bash
# Run tests
npm test

# Run linting
npm run lint
```

---

## Production Deployment

### Complete Deployment Checklist

- [ ] Frontend files prepared and tested locally
- [ ] Three.js library configured (CDN or local)
- [ ] API endpoints updated for production
- [ ] GitHub Pages enabled and working
- [ ] Backend server deployed and tested
- [ ] Environment variables configured
- [ ] CORS properly configured
- [ ] SSL/HTTPS enabled (automatic on GitHub Pages, Railway, Heroku)
- [ ] Monitoring and logging configured
- [ ] Error handling tested
- [ ] Performance optimized
- [ ] Documentation updated with actual URLs

### Multi-Environment Configuration

Create separate configuration files:

**development.env:**
```env
PORT=3000
NODE_ENV=development
PYTHON_API_URL=http://localhost:8000
```

**production.env:**
```env
PORT=3000
NODE_ENV=production
PYTHON_API_URL=https://python-api.example.com
```

Load in server.js:
```javascript
require('dotenv').config({
  path: `.env.${process.env.NODE_ENV || 'development'}`
});
```

---

## Environment Configuration

### API Server Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `PORT` | Server port | `3000` |
| `PYTHON_API_URL` | Python backend URL | `http://localhost:8000` |
| `NODE_ENV` | Environment | `production` or `development` |
| `CORS_ORIGIN` | CORS allowed origins | `https://yourdomain.com` |

### Frontend Configuration

Update API endpoint detection in `js/main.js`:
```javascript
async detectAPIServer() {
    const endpoints = [
        'https://api.gearengine.example.com',
        'https://your-app-name.up.railway.app',
        'http://localhost:3000',
    ];
    // ... rest of method
}
```

---

## Troubleshooting

### CORS Errors

**Problem:** "Access to XMLHttpRequest denied"

**Solution:**
1. Ensure your backend has CORS enabled
2. Update `api-client.js` with correct API URL
3. Check CORS_ORIGIN environment variable

### API Not Found

**Problem:** 404 errors when calling API

**Solution:**
1. Verify API server is running
2. Check API URL in `js/api-client.js`
3. Ensure Python backend is responding at expected endpoint
4. Check network tab in browser DevTools

### GitHub Pages 404 on Refresh

**Problem:** Page works on first load but 404 on refresh

**Solution:**
Create `.nojekyll` file in root:
```bash
touch .nojekyll
git add .nojekyll
git commit -m "Add nojekyll"
git push origin main
```

### Three.js Not Loading

**Problem:** "THREE is not defined"

**Solution:**
1. Check if Three.js CDN is accessible
2. Update `index.html` with correct CDN link
3. Or download and include locally
4. Check browser console for network errors

### Slow Performance

**Solutions:**
1. Enable gzip compression on server
2. Minimize CSS/JS files
3. Optimize 3D rendering quality settings
4. Consider API response caching

### Backend Connection Issues

**Check backend health:**
```bash
# Test backend locally
curl http://localhost:3000/api/health

# If deployed
curl https://your-api-server.com/api/health
```

Should return:
```json
{"status":"ok","message":"Gear Engine API Server is running"}
```

---

## Next Steps

1. **Monitor your application:**
   - Set up error tracking (Sentry, LogRocket)
   - Enable analytics
   - Monitor API response times

2. **Improve performance:**
   - Implement caching strategies
   - Optimize database queries (if using Python FastAPI backend)
   - Consider CDN for static assets

3. **Scale for production:**
   - Set up load balancing
   - Implement rate limiting
   - Use managed services for Python backend

4. **Maintain and update:**
   - Regularly update dependencies
   - Monitor for security vulnerabilities
   - Keep documentation updated

---

## Support & Resources

- **GitHub Issues:** Report bugs and request features
- **Documentation:** See `README.md` for usage guide
- **API Docs:** See backend API documentation
- **Community:** Contact the maintainers for support

---

## License

This project is licensed under the MIT License - see LICENSE file for details.
