/**
 * Gear Engine API Server
 * Express.js backend for gear generation and export
 * 
 * This server acts as a bridge between the web frontend and the Python backend.
 * It can be deployed on Heroku, Railway, Vercel, or any Node.js hosting platform.
 */

const express = require('express');
const cors = require('cors');
const bodyParser = require('body-parser');
const axios = require('axios');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 3000;
const PYTHON_API_URL = process.env.PYTHON_API_URL || 'http://localhost:8000';

// ========================================
// Middleware
// ========================================

app.use(cors());
app.use(bodyParser.json({ limit: '50mb' }));
app.use(bodyParser.urlencoded({ limit: '50mb', extended: true }));

// Request logging
app.use((req, res, next) => {
    console.log(`${new Date().toISOString()} - ${req.method} ${req.path}`);
    next();
});

// ========================================
// Health Check
// ========================================

app.get('/api/health', (req, res) => {
    res.json({
        status: 'ok',
        message: 'Gear Engine API Server is running',
        timestamp: new Date().toISOString(),
    });
});

// ========================================
// Gear Generation Endpoint
// ========================================

app.post('/api/gear/generate', async (req, res) => {
    try {
        const { gear_type, parameters } = req.body;

        if (!gear_type || !parameters) {
            return res.status(400).json({
                success: false,
                error: 'Missing gear_type or parameters',
            });
        }

        // Validate gear type
        const validTypes = [
            'spur',
            'helical',
            'bevel',
            'internal',
            'planetary',
            'rack',
            'worm',
        ];
        if (!validTypes.includes(gear_type)) {
            return res.status(400).json({
                success: false,
                error: `Invalid gear type: ${gear_type}`,
            });
        }

        // Call Python backend
        const pythonResponse = await axios.post(
            `${PYTHON_API_URL}/api/gear/generate`,
            { gear_type, parameters },
            { timeout: 30000 }
        );

        res.json(pythonResponse.data);
    } catch (error) {
        console.error('Generation error:', error.message);
        res.status(500).json({
            success: false,
            error: error.message || 'Gear generation failed',
        });
    }
});

// ========================================
// Gear Validation Endpoint
// ========================================

app.post('/api/gear/validate', async (req, res) => {
    try {
        const { gear_type, parameters } = req.body;

        if (!gear_type || !parameters) {
            return res.status(400).json({
                valid: false,
                errors: ['Missing gear_type or parameters'],
            });
        }

        // Call Python backend
        const pythonResponse = await axios.post(
            `${PYTHON_API_URL}/api/gear/validate`,
            { gear_type, parameters },
            { timeout: 5000 }
        );

        res.json(pythonResponse.data);
    } catch (error) {
        console.error('Validation error:', error.message);
        res.status(500).json({
            valid: false,
            errors: [error.message || 'Validation failed'],
        });
    }
});

// ========================================
// Gear Info Endpoint
// ========================================

app.post('/api/gear/info', async (req, res) => {
    try {
        const { gear_type, parameters } = req.body;

        if (!gear_type || !parameters) {
            return res.status(400).json({
                success: false,
                error: 'Missing gear_type or parameters',
            });
        }

        // Call Python backend
        const pythonResponse = await axios.post(
            `${PYTHON_API_URL}/api/gear/info`,
            { gear_type, parameters },
            { timeout: 10000 }
        );

        res.json(pythonResponse.data);
    } catch (error) {
        console.error('Info error:', error.message);
        res.status(500).json({
            success: false,
            error: error.message || 'Failed to get gear info',
        });
    }
});

// ========================================
// Export STEP Endpoint
// ========================================

app.post('/api/gear/export/step', async (req, res) => {
    try {
        const gearData = req.body;

        if (!gearData) {
            return res.status(400).json({
                success: false,
                error: 'Missing gear data',
            });
        }

        // Call Python backend and get file
        const pythonResponse = await axios.post(
            `${PYTHON_API_URL}/api/gear/export/step`,
            gearData,
            {
                timeout: 30000,
                responseType: 'arraybuffer',
            }
        );

        // Set headers and send file
        res.setHeader('Content-Type', 'application/step');
        res.setHeader(
            'Content-Disposition',
            'attachment; filename="gear.step"'
        );
        res.send(pythonResponse.data);
    } catch (error) {
        console.error('STEP export error:', error.message);
        res.status(500).json({
            success: false,
            error: error.message || 'STEP export failed',
        });
    }
});

// ========================================
// Export STL Endpoint
// ========================================

app.post('/api/gear/export/stl', async (req, res) => {
    try {
        const gearData = req.body;

        if (!gearData) {
            return res.status(400).json({
                success: false,
                error: 'Missing gear data',
            });
        }

        // Call Python backend and get file
        const pythonResponse = await axios.post(
            `${PYTHON_API_URL}/api/gear/export/stl`,
            gearData,
            {
                timeout: 30000,
                responseType: 'arraybuffer',
            }
        );

        // Set headers and send file
        res.setHeader('Content-Type', 'application/octet-stream');
        res.setHeader(
            'Content-Disposition',
            'attachment; filename="gear.stl"'
        );
        res.send(pythonResponse.data);
    } catch (error) {
        console.error('STL export error:', error.message);
        res.status(500).json({
            success: false,
            error: error.message || 'STL export failed',
        });
    }
});

// ========================================
// Test Endpoint
// ========================================

app.get('/api/test', (req, res) => {
    res.json({
        message: 'API Server Test Endpoint',
        pythonApiUrl: PYTHON_API_URL,
        nodeVersion: process.version,
    });
});

// ========================================
// 404 Handler
// ========================================

app.use((req, res) => {
    res.status(404).json({
        error: 'Not Found',
        path: req.path,
        method: req.method,
    });
});

// ========================================
// Error Handler
// ========================================

app.use((err, req, res, next) => {
    console.error('Error:', err);
    res.status(500).json({
        error: 'Internal Server Error',
        message: process.env.NODE_ENV === 'development' ? err.message : undefined,
    });
});

// ========================================
// Start Server
// ========================================

app.listen(PORT, () => {
    console.log(`
╔════════════════════════════════════════════╗
║  Gear Engine API Server                    ║
╠════════════════════════════════════════════╣
║  Status: Running                           ║
║  Port: ${PORT}
║  Python API: ${PYTHON_API_URL}
║  Environment: ${process.env.NODE_ENV || 'development'}
╚════════════════════════════════════════════╝
    `);
});

// Handle graceful shutdown
process.on('SIGTERM', () => {
    console.log('SIGTERM received, shutting down gracefully...');
    process.exit(0);
});

module.exports = app;
