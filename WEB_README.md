# Comprehensive README for Gear Engine Web Interface

## 🚀 Gear Engine - Professional Web-Based Gear Generator

Gear Engine is a complete, open-source web application for designing and generating precision gears. It combines a modern web interface with powerful computational backend to provide professional gear generation capabilities accessible to anyone.

### Features

✨ **7 Gear Types** - Spur, Helical, Bevel, Internal, Planetary, Rack, and Worm gears  
🎨 **3D Visualization** - Real-time interactive gear preview with rotation controls  
📥 **Multiple Export Formats** - Download as STEP (CAD) or STL (3D printing)  
📱 **Fully Responsive** - Works seamlessly on desktop, tablet, and mobile  
⚡ **Real-Time Validation** - Instant parameter checking and constraints enforcement  
🔓 **100% Open Source** - MIT licensed, free to use and modify  
🌐 **Cloud-Ready** - Deploy anywhere with provided configuration files  
📚 **Comprehensive Documentation** - Detailed guides for all gear types and parameters  

---

## Quick Start

### Local Development

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/gear_engine.git
cd gear_engine

# 2. Install Node.js dependencies
npm install

# 3. Create .env file
cp .env.example .env

# 4. Ensure Python backend is running (in separate terminal)
# See DEPLOYMENT_GUIDE.md for Python backend setup

# 5. Start the development server
npm run dev

# Application will be available at http://localhost:3000
```

### Production Deployment

See [WEB_DEPLOYMENT_GUIDE.md](WEB_DEPLOYMENT_GUIDE.md) for complete deployment instructions including:
- GitHub Pages frontend deployment
- Backend deployment on Railway, Heroku, AWS, or Docker
- Environment configuration
- Troubleshooting guide

---

## Project Structure

```
gear_engine/
├── index.html                           # Main HTML file with all sections
├── styles/
│   ├── main.css                        # Core styling and layout
│   └── responsive.css                  # Mobile and responsive design
├── js/
│   ├── api-client.js                   # API communication layer
│   ├── 3d-viewer.js                    # Three.js 3D visualization
│   ├── form-manager.js                 # Form handling and validation
│   ├── main.js                         # Application logic and initialization
│   └── three.min.js                    # Three.js library (CDN fallback)
├── server.js                            # Node.js Express backend server
├── package.json                         # Node.js dependencies
├── .env.example                         # Environment variables template
├── WEB_DEPLOYMENT_GUIDE.md             # Complete deployment guide
├── .github/
│   └── workflows/
│       ├── deploy-frontend.yml         # GitHub Actions for GitHub Pages
│       └── deploy-backend.yml          # GitHub Actions for backend
├── core/                                # Python modules (existing)
├── gears/                               # Python gear implementations
├── profiles/                            # Gear tooth profiles
├── export/                              # Export functionality
├── interfaces/                          # API and CLI interfaces
└── tests/                               # Test suite
```

---

## Architecture

The application uses a three-tier architecture:

```
┌─────────────────────────────────────┐
│    Frontend (GitHub Pages)           │
│  HTML5 + CSS3 + JavaScript + Three.js│
└──────────────┬──────────────────────┘
               │ HTTP/REST API
┌──────────────▼──────────────────────┐
│  Node.js Express Backend Server      │
│  (Railway, Heroku, or self-hosted)  │
└──────────────┬──────────────────────┘
               │ HTTP/REST API
┌──────────────▼──────────────────────┐
│  Python Backend (FastAPI)            │
│  Gear generation and export logic    │
└─────────────────────────────────────┘
```

### Component Details

**Frontend (`index.html` + CSS + JS)**
- Landing page with features showcase
- Interactive gear generator with dynamic forms
- 3D visualization using Three.js
- Export functionality for STEP and STL
- Comprehensive documentation
- Responsive design for all devices

**Node.js Server (`server.js`)**
- Express.js REST API server
- Proxy between frontend and Python backend
- Request validation and error handling
- CORS configuration for GitHub Pages
- Can be deployed independently

**Python Backend** (existing modules)
- Actual gear generation algorithms
- Mathematical models for all 7 gear types
- STEP and STL file export
- Parameter validation
- ISO standard compliance

---

## Using the Web Interface

### Home Page
- Overview of Gear Engine capabilities
- Feature highlights
- Quick start button
- Call-to-action for generator

### Generator Page
**Left Panel - Parameters:**
1. Select gear type from buttons
2. Fill in gear-specific parameters
3. Use tooltips for parameter guidance
4. Click "Generate Gear"

**Right Panel - Preview & Export:**
1. View 3D gear model
2. Rotate with mouse drag
3. Zoom with mouse wheel
4. Download as STEP or STL

### Documentation
Comprehensive guides for:
- Each gear type (Spur, Helical, Bevel, Internal, Planetary, Rack, Worm)
- Parameter definitions and ranges
- ISO standards (53, 21771)
- Export formats and usage
- Design guidelines
- Manufacturing notes

### About
- Project information
- Technology stack
- Key capabilities
- Standards compliance
- Community information

---

## Gear Types Reference

### Spur Gear
- **Best for:** Parallel shafts with high efficiency
- **Key parameters:** teeth, module, pressure angle, face width, bore
- **Load capacity:** High
- **Noise level:** Moderate-High

### Helical Gear
- **Best for:** Smooth, quiet operation
- **Key parameters:** teeth, module, pressure angle, helix angle, face width, bore
- **Load capacity:** High
- **Noise level:** Low

### Bevel Gear
- **Best for:** Intersecting shafts (perpendicular or angled)
- **Key parameters:** teeth, module, pressure angle, pitch angle, face width
- **Load capacity:** Moderate-High
- **Noise level:** Moderate

### Internal Gear
- **Best for:** Compact planetary systems
- **Key parameters:** teeth, module, pressure angle, rim thickness, face width
- **Load capacity:** Moderate
- **Noise level:** Low

### Planetary Gear
- **Best for:** Multi-speed transmissions, compact design
- **Key parameters:** sun/planet/ring teeth, module, number of planets
- **Load capacity:** High
- **Noise level:** Low

### Rack Gear
- **Best for:** Converting rotary to linear motion
- **Key parameters:** teeth, module, pressure angle, length, height
- **Load capacity:** Moderate
- **Noise level:** Moderate

### Worm Gear
- **Best for:** High reduction ratios, self-locking applications
- **Key parameters:** threads, module, lead angle, diameter, length
- **Load capacity:** Low-Moderate
- **Noise level:** Low-Moderate

---

## API Endpoints

The backend server provides the following REST API endpoints:

### Health Check
```
GET /api/health
Response: { status: "ok", message: "...", timestamp: "..." }
```

### Generate Gear
```
POST /api/gear/generate
Body: { gear_type: "spur", parameters: {...} }
Response: { success: true, vertices: [], faces: [], properties: {...} }
```

### Validate Parameters
```
POST /api/gear/validate
Body: { gear_type: "spur", parameters: {...} }
Response: { valid: true, errors: [] }
```

### Get Gear Info
```
POST /api/gear/info
Body: { gear_type: "spur", parameters: {...} }
Response: { properties: { pitch_diameter: 40, ... } }
```

### Export STEP
```
POST /api/gear/export/step
Body: { ...gear_data }
Response: Binary STEP file
```

### Export STL
```
POST /api/gear/export/stl
Body: { ...gear_data }
Response: Binary STL file
```

---

## Development

### Prerequisites
- Node.js 14+ and npm
- Python 3.8+ (for backend)
- Git

### Setup

```bash
# Install frontend dependencies
npm install

# Install Python dependencies (if running backend locally)
pip install -r requirements.txt

# Create environment file
cp .env.example .env
```

### Running Locally

**Terminal 1 - Python Backend:**
```bash
python -m interfaces.fastapi_app
# Runs on http://localhost:8000
```

**Terminal 2 - Node.js Server:**
```bash
npm run dev
# Runs on http://localhost:3000
```

**Terminal 3 - Python Tests (optional):**
```bash
pytest tests/
```

### Coding Standards

- Use ES6+ for JavaScript
- Follow PEP 8 for Python
- Add comments for complex logic
- Write tests for new features
- Keep commits atomic and well-described

---

## Deployment

### GitHub Pages (Frontend)
1. Configure repository settings
2. Enable GitHub Pages from main branch
3. Update API endpoints in code
4. GitHub Actions automatically deploys on push

See [WEB_DEPLOYMENT_GUIDE.md](WEB_DEPLOYMENT_GUIDE.md) for detailed instructions.

### Backend (Choose one)

**Railway (Recommended):**
```bash
# Simple, one-command deployment
vercel
```

**Heroku:**
```bash
heroku create gear-engine-api
git push heroku main
```

**Docker:**
```bash
docker build -f Dockerfile.backend -t gear-engine-api .
docker run -p 3000:3000 gear-engine-api
```

**Replit:**
- Fork to Replit
- Run setup script
- Configure `.env`
- Done!

---

## Configuration

### Environment Variables

Create `.env` file (copy from `.env.example`):

```env
PORT=3000
NODE_ENV=development
PYTHON_API_URL=http://localhost:8000
CORS_ORIGIN=*
```

For production, update:
```env
NODE_ENV=production
PYTHON_API_URL=https://your-api-server.com
CORS_ORIGIN=https://yourusername.github.io
```

### Customization

**Update API endpoint detection (`js/main.js`):**
```javascript
async detectAPIServer() {
    const endpoints = [
        'https://your-api-server.com',
        'http://localhost:3000',
    ];
    // ...
}
```

**Customize styling (`styles/main.css`):**
```css
:root {
    --primary-color: #4A90E2;      /* Change brand color */
    --dark-bg: #0F1419;             /* Change background */
    /* ... more variables ... */
}
```

---

## Troubleshooting

### Issue: "API Server Not Available"
- Ensure Python backend is running
- Check Node.js server is running
- Verify API URL in browser console
- Check CORS configuration

### Issue: "THREE is not defined"
- Verify Three.js CDN is accessible
- Check network tab in DevTools
- Update Three.js link in HTML

### Issue: GitHub Pages 404 on refresh
- Add `.nojekyll` file to root
- Ensure `index.html` is in root directory
- Check GitHub Pages settings

### Issue: Slow 3D rendering
- Reduce geometry complexity
- Check browser GPU acceleration
- Lower animation frame rate
- Optimize Three.js scene

### Issue: Export files not downloading
- Check browser download settings
- Verify API is responding correctly
- Check file size limits
- Test with different file format

---

## Performance Optimization

- **Frontend:** Minify CSS/JS, compress images, lazy load content
- **Backend:** Cache API responses, implement rate limiting
- **3D:** Use LOD (Level of Detail), optimize geometry
- **Database:** Index queries, implement caching strategy

---

## Security Considerations

- Validate all user input on backend
- Implement rate limiting to prevent abuse
- Use HTTPS for all production deployments
- Keep dependencies updated
- Implement authentication if needed for future features
- Sanitize file uploads

---

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes
4. Add tests if applicable
5. Commit with clear messages: `git commit -m 'Add amazing feature'`
6. Push to branch: `git push origin feature/amazing-feature`
7. Open a Pull Request

### Development Guidelines
- Write clean, readable code
- Follow project style guides
- Add inline comments for complex logic
- Test thoroughly before submitting PR
- Update documentation as needed

---

## License

This project is licensed under the MIT License - see the LICENSE file for details.

```
MIT License - Free to use, modify, and distribute
```

---

## Support & Resources

- **Issues & Feature Requests:** GitHub Issues
- **Documentation:** This README + WEB_DEPLOYMENT_GUIDE.md
- **API Documentation:** See `server.js` comments
- **Backend Docs:** See Python modules documentation
- **Community:** Contributions and feedback welcome!

---

## Roadmap

Future enhancements planned:

- [ ] WebAssembly Python backend for fully client-side generation
- [ ] More gear types (Harmonic, Cycloidal)
- [ ] Gear pair meshing visualization
- [ ] Load analysis and tooth stress calculation
- [ ] Custom tooth profiles
- [ ] Material library with properties
- [ ] Manufacturing tolerances
- [ ] Assembly animations
- [ ] Multi-language support
- [ ] Mobile app (React Native)
- [ ] Desktop app (Electron)

---

## Credits

- **Original Developer:** Gear Engine Contributors
- **Three.js:** For 3D visualization capabilities
- **FastAPI:** For Python backend framework
- **Express.js:** For Node.js server
- **ISO Standards:** For gear tooth geometry specifications

---

## Changelog

### Version 1.0.0 (Initial Release)
- ✅ 7 gear types implemented
- ✅ 3D visualization with Three.js
- ✅ STEP and STL export
- ✅ Responsive web interface
- ✅ Documentation and tutorials
- ✅ GitHub Pages deployment
- ✅ Multi-platform backend deployment

---

**Made with ❤️ for engineers, makers, and students worldwide**

For more information, visit: [GitHub Repository](https://github.com/yourusername/gear_engine)
