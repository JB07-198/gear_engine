# Gear Engine Web - Quick Start Guide

Get your Gear Engine web application up and running in minutes!

## 🚀 Fastest Path to Deployment (5 minutes)

### Option 1: GitHub Pages + Railway (Easiest)

**Step 1: Set up GitHub Pages (2 min)**
```bash
# Push code to GitHub
git push origin main

# Go to repository → Settings → Pages
# Select "Deploy from a branch"
# Choose "main" and root "/"
# Save
```

Your frontend is now live at: `https://yourusername.github.io/gear_engine/`

**Step 2: Deploy Backend to Railway (3 min)**
1. Go to https://railway.app
2. Click "Create New Project"
3. Choose "Deploy from GitHub"
4. Select your gear_engine repository
5. Wait for deployment to complete

Update `js/main.js` API URL:
```javascript
apiClient.setBaseUrl('https://your-railway-app.up.railway.app/api');
```

**Done!** Your app is now live and fully functional.

---

## 🏃 Quick Local Development (5 minutes)

```bash
# 1. Clone and setup
git clone https://github.com/yourusername/gear_engine.git
cd gear_engine

# 2. Install and run
npm install
npm run dev

# 3. In another terminal, start Python backend
python -m interfaces.fastapi_app

# 4. Open http://localhost:3000 in browser
```

---

## 📋 Pre-Deployment Checklist

- [ ] All JavaScript files in `js/` folder
- [ ] All CSS files in `styles/` folder  
- [ ] `index.html` in root directory
- [ ] `server.js` for backend
- [ ] `package.json` with dependencies
- [ ] `.env.example` as template
- [ ] GitHub Actions workflows configured
- [ ] `.nojekyll` file in root (for GitHub Pages)

---

## ⚡ Environment Setup

**Create `.env` file:**
```bash
cp .env.example .env
```

**Edit `.env` for your setup:**
```env
PORT=3000
NODE_ENV=development
PYTHON_API_URL=http://localhost:8000  # Local
# PYTHON_API_URL=https://your-api.railway.app  # Production
```

---

## 🌐 Update Frontend API Endpoint

**In `js/main.js`, update the `detectAPIServer` function:**

```javascript
async detectAPIServer() {
    const endpoints = [
        'https://your-railway-app.up.railway.app',  // Add your backend URL
        'http://localhost:3000',
    ];
    
    for (const endpoint of endpoints) {
        try {
            const response = await fetch(`${endpoint}/api/health`);
            if (response.ok) {
                apiClient.setBaseUrl(`${endpoint}/api`);
                return;
            }
        } catch (error) {
            // Continue
        }
    }
}
```

---

## 🔧 Manual Configuration (If Needed)

**Set API endpoint directly:**
```javascript
// In js/main.js, add after apiClient creation:
apiClient.setBaseUrl('https://your-api-server.com/api');
```

**Or in HTML before loading scripts:**
```html
<script>
  window.API_BASE_URL = 'https://your-api-server.com/api';
</script>
```

---

## 📦 Install Three.js

**Option A: CDN (Recommended)**
Update `index.html`:
```html
<!-- Replace: -->
<script src="js/three.min.js"></script>

<!-- With: -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
```

**Option B: Local Download**
```bash
# Download and save to js/three.min.js
curl -o js/three.min.js \
  https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js
```

---

## 🧪 Test Your Setup

```bash
# Test health endpoint
curl http://localhost:3000/api/health

# Test gear generation
curl -X POST http://localhost:3000/api/gear/generate \
  -H "Content-Type: application/json" \
  -d '{
    "gear_type": "spur",
    "parameters": {
      "teeth": 20,
      "module": 2,
      "pressure_angle": 20,
      "face_width": 10,
      "bore_diameter": 10
    }
  }'
```

Expected response:
```json
{
  "success": true,
  "properties": { ... },
  "vertices": [ ... ],
  "faces": [ ... ]
}
```

---

## 🚢 Deployment Platforms

### Railway (Recommended)
- Free tier with $5/month credit
- Auto-deploys on git push
- Easy environment variables
- Built-in monitoring

### Heroku
- Free tier ended but still available with credits
- Works with Procfile
- Easy to set up
- Good for learning

### Docker + Any Cloud
- AWS ECS
- Google Cloud Run
- Azure Container Instances
- DigitalOcean App Platform

### Vercel (Serverless)
- Serverless deployment
- Works with serverless functions
- Good for lightweight APIs

---

## 🔍 Verify Deployment

**Check frontend:**
```bash
curl https://yourusername.github.io/gear_engine/
```

**Check backend:**
```bash
curl https://your-railway-app.up.railway.app/api/health
```

Both should return 200 status code ✅

---

## 🐛 Quick Troubleshooting

| Problem | Solution |
|---------|----------|
| **API 404** | Update API URL in `js/main.js` |
| **CORS error** | Ensure backend CORS is enabled |
| **THREE undefined** | Check Three.js CDN in HTML |
| **404 on page refresh** | Add `.nojekyll` file to root |
| **Slow rendering** | Check WebGL support in browser |

---

## 📚 Full Documentation

- **Deployment:** See `WEB_DEPLOYMENT_GUIDE.md`
- **Architecture:** See `WEB_README.md`
- **API Docs:** See `server.js` comments
- **Python Docs:** See existing `README.md`

---

## 🎯 Next Steps

1. **Customize UI:** Edit CSS in `styles/`
2. **Add features:** Extend JavaScript in `js/`
3. **Monitor app:** Set up error tracking (Sentry, etc.)
4. **Scale:** Implement caching, optimize queries
5. **Promote:** Share your gear generator!

---

## 💡 Pro Tips

- Use environment variables for different deployments
- Set up GitHub Actions for auto-deployment
- Monitor API response times
- Cache 3D models for faster rendering
- Implement user feedback system
- Monitor error logs regularly

---

## 🆘 Need Help?

- Check `WEB_DEPLOYMENT_GUIDE.md` for detailed setup
- Review `WEB_README.md` for architecture overview
- Check browser console for JavaScript errors
- Test API endpoints with curl/Postman
- Check GitHub Actions for deployment logs

---

**You're ready to deploy! 🚀**

Now visit your GitHub Pages URL and start generating gears!

For complete documentation, see [WEB_DEPLOYMENT_GUIDE.md](WEB_DEPLOYMENT_GUIDE.md)
