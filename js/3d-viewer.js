/**
 * 3D Viewer using Three.js
 * Handles 3D visualization of generated gears
 */

class GearViewer3D {
    constructor(canvasElement) {
        this.canvas = canvasElement;
        this.width = canvasElement.clientWidth;
        this.height = canvasElement.clientHeight;
        this.scene = null;
        this.camera = null;
        this.renderer = null;
        this.gearMesh = null;
        this.controls = null;
        this.animationId = null;

        this.init();
    }

    init() {
        // Scene setup
        this.scene = new THREE.Scene();
        this.scene.background = new THREE.Color(0x1a1f2b);

        // Camera setup
        this.camera = new THREE.PerspectiveCamera(
            75,
            this.width / this.height,
            0.1,
            1000
        );
        this.camera.position.set(0, 0, 100);

        // Renderer setup
        this.renderer = new THREE.WebGLRenderer({
            antialias: true,
            alpha: true,
        });
        this.renderer.setSize(this.width, this.height);
        this.renderer.setPixelRatio(window.devicePixelRatio);
        this.canvas.appendChild(this.renderer.domElement);

        // Lighting
        this.setupLighting();

        // Basic controls (simplified version without external library)
        this.setupControls();

        // Handle window resize
        window.addEventListener('resize', () => this.onWindowResize());

        // Start animation loop
        this.animate();
    }

    setupLighting() {
        // Ambient light
        const ambientLight = new THREE.AmbientLight(0xffffff, 0.6);
        this.scene.add(ambientLight);

        // Directional lights
        const directionalLight1 = new THREE.DirectionalLight(0xffffff, 0.8);
        directionalLight1.position.set(100, 100, 100);
        this.scene.add(directionalLight1);

        const directionalLight2 = new THREE.DirectionalLight(0xffffff, 0.4);
        directionalLight2.position.set(-100, -100, 50);
        this.scene.add(directionalLight2);

        // Point light
        const pointLight = new THREE.PointLight(0x4a90e2, 0.5);
        pointLight.position.set(50, 50, 50);
        this.scene.add(pointLight);
    }

    setupControls() {
        this.controls = {
            mouseDown: false,
            previousMousePosition: { x: 0, y: 0 },
        };

        const canvas = this.renderer.domElement;

        canvas.addEventListener('mousedown', (e) => {
            this.controls.mouseDown = true;
            this.controls.previousMousePosition = { x: e.clientX, y: e.clientY };
        });

        canvas.addEventListener('mousemove', (e) => {
            if (this.controls.mouseDown && this.gearMesh) {
                const deltaX =
                    e.clientX - this.controls.previousMousePosition.x;
                const deltaY =
                    e.clientY - this.controls.previousMousePosition.y;

                this.gearMesh.rotation.y += deltaX * 0.01;
                this.gearMesh.rotation.x += deltaY * 0.01;

                this.controls.previousMousePosition = { x: e.clientX, y: e.clientY };
            }
        });

        canvas.addEventListener('mouseup', () => {
            this.controls.mouseDown = false;
        });

        canvas.addEventListener('mouseleave', () => {
            this.controls.mouseDown = false;
        });

        // Mouse wheel zoom
        canvas.addEventListener('wheel', (e) => {
            e.preventDefault();
            const zoomSpeed = 5;
            if (e.deltaY < 0) {
                this.camera.position.z -= zoomSpeed;
            } else {
                this.camera.position.z += zoomSpeed;
            }
            this.camera.position.z = Math.max(20, Math.min(500, this.camera.position.z));
        });
    }

    /**
     * Display a gear mesh
     */
    displayGear(gearData) {
        // Remove existing gear
        if (this.gearMesh) {
            this.scene.remove(this.gearMesh);
        }

        // Create gear mesh from data
        this.gearMesh = this.createGearMesh(gearData);
        this.scene.add(this.gearMesh);

        // Auto-fit camera
        this.fitCameraToObject();
    }

    /**
     * Create a gear mesh from geometry data
     */
    createGearMesh(gearData) {
        // Parse geometry data (assuming it comes in a standard format)
        const geometry = this.parseGeometry(gearData);

        // Create material
        const material = new THREE.MeshPhongMaterial({
            color: 0x4a90e2,
            shininess: 100,
            emissive: 0x1a1f2b,
        });

        // Create and return mesh
        const mesh = new THREE.Mesh(geometry, material);

        // Compute bounding box for proper scaling
        geometry.computeBoundingBox();
        geometry.center();

        return mesh;
    }

    /**
     * Parse geometry from gearData
     */
    parseGeometry(gearData) {
        const geometry = new THREE.BufferGeometry();

        // If gearData contains vertices and faces
        if (gearData.vertices && gearData.faces) {
            const vertices = new Float32Array(gearData.vertices.flat());
            const faces = new Uint32Array(gearData.faces.flat());

            geometry.setAttribute('position', new THREE.BufferAttribute(vertices, 3));
            geometry.setIndex(new THREE.BufferAttribute(faces, 1));
            geometry.computeVertexNormals();
        } else {
            // Fallback: create a simple cylinder to represent the gear
            const baseGeometry = new THREE.CylinderGeometry(
                50,
                50,
                20,
                32
            );
            return baseGeometry;
        }

        return geometry;
    }

    /**
     * Fit camera to object
     */
    fitCameraToObject() {
        if (!this.gearMesh) return;

        const bbox = new THREE.Box3().setFromObject(this.gearMesh);
        const center = bbox.getCenter(new THREE.Vector3());
        const size = bbox.getSize(new THREE.Vector3());

        const maxDim = Math.max(size.x, size.y, size.z);
        const fov = this.camera.fov * (Math.PI / 180);
        let cameraZ = Math.abs(maxDim / 2 / Math.tan(fov / 2));

        cameraZ *= 1.5; // Add padding

        this.camera.position.copy(center);
        this.camera.position.z += cameraZ;
        this.camera.lookAt(center);
    }

    /**
     * Reset view
     */
    resetView() {
        if (this.gearMesh) {
            this.gearMesh.rotation.set(0, 0, 0);
            this.fitCameraToObject();
        }
    }

    /**
     * Animation loop
     */
    animate = () => {
        this.animationId = requestAnimationFrame(this.animate);

        // Auto-rotate gear when not being dragged
        if (this.gearMesh && !this.controls.mouseDown) {
            this.gearMesh.rotation.y += 0.005;
        }

        this.renderer.render(this.scene, this.camera);
    };

    /**
     * Handle window resize
     */
    onWindowResize = () => {
        this.width = this.canvas.clientWidth;
        this.height = this.canvas.clientHeight;

        this.camera.aspect = this.width / this.height;
        this.camera.updateProjectionMatrix();

        this.renderer.setSize(this.width, this.height);
    };

    /**
     * Clean up
     */
    dispose() {
        if (this.animationId) {
            cancelAnimationFrame(this.animationId);
        }
        if (this.renderer) {
            this.renderer.dispose();
            this.canvas.removeChild(this.renderer.domElement);
        }
    }

    /**
     * Take a screenshot
     */
    takeScreenshot() {
        return this.renderer.domElement.toDataURL('image/png');
    }

    /**
     * Set background color
     */
    setBackgroundColor(color) {
        this.scene.background = new THREE.Color(color);
    }

    /**
     * Set gear color
     */
    setGearColor(color) {
        if (this.gearMesh && this.gearMesh.material) {
            this.gearMesh.material.color.setHex(color);
        }
    }
}

// Global gear viewer instance
let gearViewer = null;
