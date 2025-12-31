# Gear Engine - Architecture & Technical Design

## System Overview

Gear Engine is a modern, distributed three-tier web application for generating precision gears.

```
┌─────────────────────────────────────────────────────────────┐
│                    Web Browser                              │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Frontend: HTML5 + CSS3 + JavaScript + Three.js     │   │
│  │  • Interactive UI                                   │   │
│  │  • 3D Visualization                                 │   │
│  │  • Form Handling                                    │   │
│  └─────────────────────────────────────────────────────┘   │
│                          │                                  │
│                   HTTP/REST API                             │
└──────────────────────────┼──────────────────────────────────┘
                           │
          ┌────────────────┴────────────────┐
          │                                 │
          ▼                                 ▼
   ┌─────────────────┐           ┌──────────────────┐
   │  GitHub Pages   │           │  Node.js Server  │
   │  (CDN)          │           │  (Express.js)    │
   │  • Hosting      │           │  • API Gateway   │
   │  • Distribution │           │  • Routing       │
   └─────────────────┘           │  • Validation    │
                                 │  • CORS          │
                                 └────────┬─────────┘
                                          │
                            ┌─────────────┴──────────────┐
                            │                            │
                            ▼                            ▼
                  ┌────────────────────┐      ┌──────────────────┐
                  │ Python Backend     │      │   File Storage   │
                  │ (FastAPI)          │      │   • STEP Files   │
                  │ • Gear Generation  │      │   • STL Files    │
                  │ • Math Algorithms  │      │   • Temporary    │
                  │ • Validation       │      └──────────────────┘
                  │ • Export           │
                  └────────────────────┘
```

---

## Component Architecture

### 1. Frontend (Client-Side)

**Location:** Browser, GitHub Pages
**Technologies:** HTML5, CSS3, ES6+ JavaScript, Three.js
**Size:** ~150KB total (uncompressed)

#### Structure:
```
Frontend/
├── index.html              # Single HTML file (SPA)
├── styles/
│   ├── main.css           # Core styles (~5000 lines)
│   └── responsive.css     # Media queries for all devices
└── js/
    ├── api-client.js      # API communication (class: GearAPIClient)
    ├── 3d-viewer.js       # 3D visualization (class: GearViewer3D)
    ├── form-manager.js    # Form logic (class: FormManager)
    ├── main.js            # App logic (class: GearEngineApp)
    └── three.min.js       # Three.js library
```

#### Key Features:
- **Single Page Application (SPA):** No page reloads, all navigation client-side
- **Responsive Design:** Adapts to desktop, tablet, mobile
- **3D Visualization:** Real-time gear preview with rotation/zoom
- **Form Validation:** Client-side validation before submission
- **Local Storage:** Cache user preferences

#### Design Patterns:
- **Module Pattern:** Each JS file is a self-contained module
- **Observer Pattern:** Event bus for loose coupling
- **Facade Pattern:** API client abstracts HTTP complexity
- **MVC Pattern:** Separation of views, controllers, models

---

### 2. Backend Server (Node.js)

**Location:** Heroku/Railway/Docker/Self-hosted
**Technologies:** Node.js, Express.js
**Size:** ~100KB

#### Structure:
```
server.js                    # Main Express application
├── /api/health            # Health check endpoint
├── /api/gear/generate     # Gear generation request
├── /api/gear/validate     # Parameter validation
├── /api/gear/info         # Gear properties calculation
├── /api/gear/export/step  # STEP file export
└── /api/gear/export/stl   # STL file export
```

#### Key Responsibilities:
1. **Request Routing:** Direct requests to appropriate endpoints
2. **CORS Handling:** Allow requests from GitHub Pages
3. **Validation:** Validate incoming requests
4. **Proxy:** Forward requests to Python backend
5. **Response Formatting:** Standardize API responses
6. **Error Handling:** Graceful error messages
7. **Logging:** Track requests and errors

#### Middleware Stack:
```
Request
  ↓
[CORS Middleware] - Allow cross-origin requests
  ↓
[Body Parser] - Parse JSON/form data
  ↓
[Logger] - Log request details
  ↓
[Routes] - Handle specific endpoints
  ↓
[Error Handler] - Catch and format errors
  ↓
Response
```

---

### 3. Python Backend (FastAPI)

**Location:** Same server or separate deployment
**Technologies:** Python, FastAPI, existing gear modules
**Modules:** core/, gears/, profiles/, export/, standards/

#### Key Modules:
- **core/gear_factory.py:** Factory pattern for creating gears
- **core/math_utils.py:** Mathematical calculations
- **gears/*:** Specific gear implementations (Spur, Helical, etc.)
- **export/step.py:** STEP file generation
- **export/stl.py:** STL file generation
- **profiles/involute.py:** Involute tooth profile
- **standards/iso_53.py:** ISO standard compliance

#### Processing Pipeline:
```
Parameters
  ↓
[Validation] - Check parameter ranges
  ↓
[Gear Factory] - Create appropriate gear object
  ↓
[Calculation] - Compute tooth geometry
  ↓
[Profile Generation] - Create tooth profiles
  ↓
[Mesh Generation] - Create 3D mesh
  ↓
[Export] - Generate STEP or STL
  ↓
Result (Geometry + Properties)
```

---

## Data Flow

### Generate Gear Flow:

```
1. User Input (Frontend)
   ├─ Gear type selected
   ├─ Parameters entered
   └─ Generate button clicked

2. Frontend Processing
   ├─ Form validation
   ├─ Parameter bounds checking
   └─ API request preparation

3. HTTP Request (Frontend → Node.js)
   POST /api/gear/generate
   {
     "gear_type": "spur",
     "parameters": {
       "teeth": 20,
       "module": 2,
       ...
     }
   }

4. Node.js Processing
   ├─ Request validation
   ├─ CORS headers added
   └─ Forward to Python backend

5. Python Backend Processing
   ├─ Validate parameters against ISO standards
   ├─ Create gear object (factory pattern)
   ├─ Calculate tooth geometry
   ├─ Generate 3D mesh (vertices + faces)
   ├─ Calculate properties (diameter, pitch, etc.)
   └─ Return result as JSON

6. HTTP Response (Python → Node.js → Frontend)
   {
     "success": true,
     "vertices": [[x,y,z], ...],
     "faces": [[v1,v2,v3], ...],
     "properties": {
       "pitch_diameter": 40,
       "outer_diameter": 42,
       ...
     }
   }

7. Frontend Rendering
   ├─ Parse vertex and face data
   ├─ Create Three.js geometry
   ├─ Display 3D model in viewer
   ├─ Update properties panel
   └─ Enable export buttons

8. User Exports Gear
   └─ Download STEP or STL file
```

### Export Flow:

```
1. User clicks export button (STEP or STL)
   ↓
2. Frontend sends gear data to backend
   POST /api/gear/export/step or /stl
   ↓
3. Node.js forwards to Python backend
   ↓
4. Python backend generates binary file
   ├─ Create CAD/mesh model
   ├─ Serialize to STEP or STL format
   └─ Return binary blob
   ↓
5. Node.js forwards binary response
   ↓
6. Frontend receives blob
   ├─ Create download link
   ├─ Trigger browser download
   └─ User gets file
```

---

## API Specification

### Request/Response Format

**Standard Request:**
```json
{
  "gear_type": "spur|helical|bevel|internal|planetary|rack|worm",
  "parameters": {
    "teeth": number,
    "module": number,
    ...type-specific parameters...
  }
}
```

**Standard Response:**
```json
{
  "success": true|false,
  "error": "error message (if success=false)",
  "properties": {
    "pitch_diameter": number,
    "outer_diameter": number,
    "root_diameter": number,
    ...
  },
  "vertices": [[x,y,z], [x,y,z], ...],
  "faces": [[v0,v1,v2], [v0,v1,v2], ...]
}
```

### Error Handling

**Standard Error Response:**
```json
{
  "success": false,
  "error": "Descriptive error message",
  "status": 400|500,
  "timestamp": "2024-01-01T12:00:00Z"
}
```

---

## Deployment Architecture

### GitHub Pages (Frontend)
- Static hosting (no server)
- Automatic HTTPS
- CDN distribution
- Free hosting
- Auto-deploys on git push

### Node.js Backend Options

**Railway:**
```
┌──────────────┐
│  GitHub     │  Push code
│  Repository │─────────────┐
└──────────────┘             │
                             ▼
                    ┌──────────────────┐
                    │  GitHub Actions  │
                    │  (CI/CD)         │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │  Railway         │
                    │  • Node.js       │
                    │  • Python        │
                    │  • Database      │
                    └──────────────────┘
```

**Heroku:**
```
Git Push
  ↓
Heroku Dyno (Container)
  ├─ Web: Node.js Express
  └─ Worker: Python FastAPI
```

**Docker:**
```
Dockerfile.backend
  ↓
Docker Image
  ↓
Container Registry
  ↓
Cloud Platform
  ├─ AWS ECS
  ├─ Google Cloud Run
  ├─ Azure ACI
  └─ DigitalOcean
```

---

## Security Architecture

### CORS (Cross-Origin Resource Sharing)
```
Browser (GitHub Pages)
  ↓ Request with CORS headers
Server
  ↓
Checks origin against whitelist
  ↓
Allows/Denies request
  ↓
Adds Access-Control headers to response
```

**Configuration:**
```javascript
// In server.js
app.use(cors({
  origin: [
    'https://yourusername.github.io',
    'https://gear-engine.com',
    'http://localhost:3000'
  ],
  methods: ['GET', 'POST'],
  credentials: false
}));
```

### Input Validation
```
Request Parameters
  ↓
Type Checking (string, number, etc.)
  ↓
Range Validation (min/max values)
  ↓
Format Validation (regex patterns)
  ↓
Business Logic Validation (constraints)
  ↓
Accepted or Rejected
```

### Rate Limiting (Optional)
```
Request
  ↓
Check IP/User against rate limit
  ↓
Within limit? Yes → Process
                 No → Return 429 (Too Many Requests)
```

---

## Performance Optimization

### Frontend
1. **Minification:** Remove unnecessary characters from CSS/JS
2. **Code Splitting:** Load only needed code
3. **Caching:** Browser caches static assets
4. **Lazy Loading:** Load images/data as needed
5. **CDN:** Serve from edge locations

### Backend
1. **Connection Pooling:** Reuse database connections
2. **Response Caching:** Cache frequent requests
3. **Request Timeout:** Prevent hung requests (30s)
4. **Async Processing:** Non-blocking I/O
5. **Load Balancing:** Distribute load across servers

### 3D Rendering
1. **Geometry Optimization:** Reduce polygon count for simple gears
2. **Level of Detail (LOD):** Different detail levels
3. **Viewport Optimization:** Only render visible objects
4. **Shader Optimization:** Efficient GLSL code

---

## Scalability Considerations

### Horizontal Scaling (Add Servers)
```
Load Balancer
  ├─ Server 1 (Node.js)
  ├─ Server 2 (Node.js)
  └─ Server 3 (Node.js)
     ↓
  Shared Python Backend (or separate instances)
```

### Vertical Scaling (Bigger Server)
- Increase CPU cores
- Increase RAM
- Upgrade network bandwidth

### Caching Strategy
```
Browser Cache (Static assets)
  ↓
CDN Cache (Edge locations)
  ↓
Server Cache (Redis/Memcached)
  ↓
Database (Persistent storage)
```

---

## Monitoring & Logging

### Frontend Monitoring
- Error tracking (Sentry)
- Performance monitoring (Web Vitals)
- User analytics (Google Analytics)
- Browser console logs

### Backend Monitoring
- Request logging
- Error tracking
- Performance metrics
- Health checks
- Uptime monitoring (Pingdom)

### Logs Format:
```
2024-01-01T12:00:00Z [INFO] GET /api/health HTTP/1.1 200
2024-01-01T12:00:01Z [INFO] POST /api/gear/generate HTTP/1.1 200
2024-01-01T12:00:02Z [ERROR] Python backend timeout at /api/gear/export/step
```

---

## Technology Choices & Rationale

| Component | Technology | Reason |
|-----------|-----------|--------|
| Frontend Hosting | GitHub Pages | Free, secure, auto-deploy |
| Frontend UI | HTML5/CSS3/JS | Standard web technologies |
| 3D Library | Three.js | Industry standard, well-documented |
| Backend API | Express.js | Lightweight, fast, easy to deploy |
| Python Bridge | FastAPI | Modern, async-capable |
| Container | Docker | Consistent deployments |
| Process Mgr | PM2 (optional) | Node.js process management |

---

## Future Architecture Enhancements

1. **WebAssembly Python:** Compile Python to WASM for client-side generation
2. **Real-time Collaboration:** WebSocket for multi-user editing
3. **Microservices:** Split into smaller services
4. **Message Queue:** For async gear generation
5. **Database:** Store user designs and history
6. **Machine Learning:** Recommend gear combinations
7. **Mobile App:** React Native version
8. **Desktop App:** Electron version

---

## Development Workflow

```
Developer
  ↓
Edit Code (Frontend/Backend)
  ↓
npm run dev / npm start
  ↓
Local Testing (http://localhost:3000)
  ↓
Unit Tests / Integration Tests
  ↓
Commit & Push to GitHub
  ↓
GitHub Actions CI/CD
  ├─ Run tests
  ├─ Build
  └─ Deploy (if tests pass)
  ↓
Production Deployment
  ├─ GitHub Pages (frontend)
  └─ Railway/Heroku (backend)
  ↓
Monitoring & Alerting
```

---

This architecture provides:
✅ **Scalability:** Easy to add more servers
✅ **Reliability:** Separated concerns
✅ **Performance:** Optimized at each layer
✅ **Maintainability:** Clear structure
✅ **Security:** Input validation and CORS
✅ **Cost-Effectiveness:** Free/cheap hosting options
