// 3D Apartment Visualization with Three.js
class Apartment3D {
    constructor() {
        this.container = document.getElementById('apartment-3d');
        this.scene = null;
        this.camera = null;
        this.renderer = null;
        this.controls = null;
        this.rooms = {};
        this.devices = {};
        this.lights = {};
        this.sensors = [];
        
        this.init();
        this.createApartment();
        this.createSensorsPanel();
        this.startSensorUpdates();
        this.animate();
    }

    init() {
        // Scene
        this.scene = new THREE.Scene();
        this.scene.background = new THREE.Color(0x0a0e27);
        this.scene.fog = new THREE.Fog(0x0a0e27, 50, 100);

        // Camera
        this.camera = new THREE.PerspectiveCamera(
            60,
            this.container.clientWidth / this.container.clientHeight,
            0.1,
            1000
        );
        this.camera.position.set(35, 30, 35);
        this.camera.lookAt(0, 0, 0);

        // Renderer
        this.renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
        this.renderer.setSize(this.container.clientWidth, this.container.clientHeight);
        this.renderer.shadowMap.enabled = true;
        this.renderer.shadowMap.type = THREE.PCFSoftShadowMap;
        this.container.appendChild(this.renderer.domElement);

        // Controls
        this.controls = new THREE.OrbitControls(this.camera, this.renderer.domElement);
        this.controls.enableDamping = true;
        this.controls.dampingFactor = 0.05;
        this.controls.maxPolarAngle = Math.PI / 2;

        // Ambient Light
        const ambientLight = new THREE.AmbientLight(0x404040, 0.5);
        this.scene.add(ambientLight);

        // Main Light
        const mainLight = new THREE.DirectionalLight(0xffffff, 0.5);
        mainLight.position.set(20, 30, 20);
        mainLight.castShadow = true;
        mainLight.shadow.mapSize.width = 2048;
        mainLight.shadow.mapSize.height = 2048;
        this.scene.add(mainLight);

        // Handle resize
        window.addEventListener('resize', () => this.onWindowResize());
    }

    createApartment() {
        // Floor
        const floorGeometry = new THREE.PlaneGeometry(60, 50);
        const floorMaterial = new THREE.MeshStandardMaterial({ 
            color: 0x1e293b,
            roughness: 0.8,
            metalness: 0.2
        });
        const floor = new THREE.Mesh(floorGeometry, floorMaterial);
        floor.rotation.x = -Math.PI / 2;
        floor.receiveShadow = true;
        this.scene.add(floor);

        // Create realistic apartment layout
        // Main entrance with outdoor area at bottom
        this.createRoom('outdoor', 0, 0, 18, 30, 8, 0x334155);
        
        // Corridors in the middle connecting all rooms
        this.createRoom('corridors', 0, 0, 6, 30, 4, 0x475569);
        
        // Left side: Bathroom (top left)
        this.createRoom('bathroom', -10, 0, -4, 8, 6, 0x475569);
        
        // Left side: Room 1 (middle left)
        this.createRoom('room1', -10, 0, 4, 8, 8, 0x475569);
        
        // Left side: Room 2 (bottom left)
        this.createRoom('room2', -10, 0, 14, 8, 8, 0x475569);
        
        // Right side: Kitchen (top right)
        this.createRoom('kitchen', 10, 0, -4, 8, 6, 0x475569);
        
        // Right side: Reception (middle right) - living room
        this.createRoom('reception', 10, 0, 4, 8, 8, 0x475569);

        // Create devices for each room
        this.createBathroomDevices();
        this.createCorridorsDevices();
        this.createReceptionDevices();
        this.createKitchenDevices();
        this.createRoom1Devices();
        this.createRoom2Devices();
        this.createOutdoorDevices();
    }

    createRoom(name, x, y, z, width, depth, color) {
        const wallHeight = 5;
        const wallThickness = 0.2;

        // Walls
        const wallMaterial = new THREE.MeshStandardMaterial({ 
            color: color,
            roughness: 0.7,
            metalness: 0.1,
            transparent: true,
            opacity: 0.6
        });

        // Back wall
        const backWall = this.createWall(width, wallHeight, wallThickness, wallMaterial);
        backWall.position.set(x, wallHeight/2, z - depth/2);
        this.scene.add(backWall);

        // Front wall
        const frontWall = this.createWall(width, wallHeight, wallThickness, wallMaterial);
        frontWall.position.set(x, wallHeight/2, z + depth/2);
        this.scene.add(frontWall);

        // Left wall
        const leftWall = this.createWall(wallThickness, wallHeight, depth, wallMaterial);
        leftWall.position.set(x - width/2, wallHeight/2, z);
        this.scene.add(leftWall);

        // Right wall
        const rightWall = this.createWall(wallThickness, wallHeight, depth, wallMaterial);
        rightWall.position.set(x + width/2, wallHeight/2, z);
        this.scene.add(rightWall);

        // Room label
        this.createRoomLabel(name, x, wallHeight + 1, z);

        this.rooms[name] = { x, y, z, width, depth };
    }

    createWall(width, height, depth, material) {
        const geometry = new THREE.BoxGeometry(width, height, depth);
        const mesh = new THREE.Mesh(geometry, material);
        mesh.castShadow = true;
        mesh.receiveShadow = true;
        return mesh;
    }

    createRoomLabel(text, x, y, z) {
        const canvas = document.createElement('canvas');
        const context = canvas.getContext('2d');
        canvas.width = 512;
        canvas.height = 128;
        
        context.fillStyle = '#6366f1';
        context.font = 'Bold 48px Arial';
        context.textAlign = 'center';
        context.fillText(text.toUpperCase(), 256, 80);
        
        const texture = new THREE.CanvasTexture(canvas);
        const material = new THREE.SpriteMaterial({ map: texture });
        const sprite = new THREE.Sprite(material);
        sprite.position.set(x, y, z);
        sprite.scale.set(4, 1, 1);
        this.scene.add(sprite);
    }
    
    createDeviceLabel(text, x, y, z) {
        const canvas = document.createElement('canvas');
        const context = canvas.getContext('2d');
        canvas.width = 256;
        canvas.height = 64;
        
        // Background with transparency
        context.fillStyle = 'rgba(15, 23, 42, 0.8)';
        context.fillRect(0, 0, canvas.width, canvas.height);
        
        // Text
        context.fillStyle = '#ffffff';
        context.font = 'Bold 24px Arial';
        context.textAlign = 'center';
        context.textBaseline = 'middle';
        context.fillText(text, 128, 32);
        
        const texture = new THREE.CanvasTexture(canvas);
        const material = new THREE.SpriteMaterial({ 
            map: texture,
            transparent: true
        });
        const sprite = new THREE.Sprite(material);
        sprite.position.set(x, y, z);
        sprite.scale.set(1.5, 0.4, 1);
        this.scene.add(sprite);
        
        return sprite;
    }

    createBathroomDevices() {
        const room = this.rooms['bathroom'];
        this.createLight('bath_light', room.x, 4, room.z);
        this.createFireSensor('bath_fire', room.x + 3, 4, room.z - 2);
        this.createHeater('bath_heater', room.x - 3, 1, room.z + 2);
        this.createFan('bath_fan', room.x + 2, 4, room.z + 2);
    }

    createCorridorsDevices() {
        const room = this.rooms['corridors'];
        // Main Light - Large single light
        this.createMainLight('corr_main_light', room.x, 4, room.z);
        // Spots Light - 3 small spot lights
        this.createSpotLight('corr_spots', room.x - 6, 4, room.z - 1);
        this.createSpotLight('corr_spots', room.x, 4, room.z + 1);
        this.createSpotLight('corr_spots', room.x + 6, 4, room.z - 1);
        this.createFireSensor('corr_fire', room.x + 12, 4, room.z);
    }

    createReceptionDevices() {
        const room = this.rooms['reception'];
        this.createLight('rec_light', room.x, 4, room.z);
        this.createWindow('rec_window', room.x + 3.8, 2.5, room.z - 2);
        this.createFireSensor('rec_fire', room.x - 3, 4, room.z - 3);
        this.createSoundSystem('rec_sound', room.x - 3, 1, room.z + 3);
        this.createAC('rec_ac', room.x + 3, 4, room.z + 3);
    }

    createKitchenDevices() {
        const room = this.rooms['kitchen'];
        this.createLight('kit_light', room.x, 4, room.z);
        this.createWindow('kit_window', room.x + 3.8, 2.5, room.z);
        this.createFan('kit_fan', room.x - 2, 4, room.z + 2);
        this.createFireSensor('kit_fire', room.x + 2, 4, room.z - 2);
    }

    createRoom1Devices() {
        const room = this.rooms['room1'];
        this.createLight('r1_light', room.x, 4, room.z);
        this.createWindow('r1_window', room.x - 3.8, 2.5, room.z);
        this.createAC('r1_ac', room.x + 3, 4, room.z - 3);
        this.createTV('r1_tv', room.x, 1.5, room.z - 3.5);
        this.createFireSensor('r1_fire', room.x + 3, 4, room.z + 3);
        this.createSoundSystem('r1_sound', room.x - 3, 1, room.z + 3);
    }

    createRoom2Devices() {
        const room = this.rooms['room2'];
        this.createLight('r2_light', room.x, 4, room.z);
        this.createAC('r2_ac', room.x + 3, 4, room.z - 3);
        this.createFireSensor('r2_fire', room.x + 3, 4, room.z + 3);
        this.createSoundSystem('r2_sound', room.x - 3, 1, room.z + 3);
    }

    createOutdoorDevices() {
        const room = this.rooms['outdoor'];
        // Create two separate outdoor lights with unique IDs
        this.createLight('out_light_1', room.x - 8, 4, room.z);
        this.createLight('out_light_2', room.x + 8, 4, room.z);
        this.createCamera('out_camera', room.x, 4.5, room.z - 3);
        this.createDoor('out_door', room.x, 0, room.z + 3.8);
    }

    // Device creation methods
    createLight(id, x, y, z) {
        // Light bulb with realistic shape
        const geometry = new THREE.SphereGeometry(0.3, 16, 16);
        const material = new THREE.MeshStandardMaterial({ 
            color: 0xffffff,
            emissive: 0x444444,
            emissiveIntensity: 0,
            metalness: 0.3,
            roughness: 0.7
        });
        const bulb = new THREE.Mesh(geometry, material);
        bulb.position.set(x, y, z);
        this.scene.add(bulb);

        // Point light with realistic warm color and LIMITED distance
        const light = new THREE.PointLight(0xffd700, 0, 8, 2);  // Warm yellow, decay=2 for realism
        light.position.set(x, y, z);
        light.castShadow = true;
        light.shadow.bias = -0.001;
        this.scene.add(light);
        
        // Add label
        const label = this.createDeviceLabel('Light', x, y - 0.8, z);

        this.devices[id] = { mesh: bulb, light: light, label: label, type: 'light' };
    }

    createMainLight(id, x, y, z) {
        // Large main light bulb
        const geometry = new THREE.SphereGeometry(0.5, 32, 32);
        const material = new THREE.MeshStandardMaterial({ 
            color: 0x64748b,
            emissive: 0x64748b,
            emissiveIntensity: 0
        });
        const bulb = new THREE.Mesh(geometry, material);
        bulb.position.set(x, y, z);
        this.scene.add(bulb);

        // Stronger point light with LIMITED distance
        const light = new THREE.PointLight(0xfbbf24, 0, 6);  // distance = 6 (only lights corridor)
        light.position.set(x, y, z);
        light.castShadow = true;
        this.scene.add(light);

        this.devices[id] = { mesh: bulb, light: light, type: 'light', isMainLight: true };
    }

    createSpotLight(id, x, y, z) {
        // Small spot light - only create if not exists
        if (!this.devices[id]) {
            // Create group for all spot lights
            this.devices[id] = { spots: [], type: 'light', isSpotGroup: true };
        }

        // Small spot bulb
        const geometry = new THREE.ConeGeometry(0.15, 0.3, 8);
        const material = new THREE.MeshStandardMaterial({ 
            color: 0x64748b,
            emissive: 0x64748b,
            emissiveIntensity: 0
        });
        const spot = new THREE.Mesh(geometry, material);
        spot.position.set(x, y, z);
        spot.rotation.x = Math.PI;
        this.scene.add(spot);

        // Spot light with LIMITED distance and angle
        const light = new THREE.SpotLight(0xfbbf24, 0, 5, Math.PI / 8);  // distance = 5, narrow angle
        light.position.set(x, y, z);
        light.target.position.set(x, 0, z);
        light.castShadow = true;
        this.scene.add(light);
        this.scene.add(light.target);

        // Add to spots array
        this.devices[id].spots.push({ mesh: spot, light: light });
    }

    createFireSensor(id, x, y, z) {
        const geometry = new THREE.CylinderGeometry(0.2, 0.2, 0.1, 16);
        const material = new THREE.MeshStandardMaterial({ 
            color: 0xef4444,
            emissive: 0xef4444,
            emissiveIntensity: 0
        });
        const sensor = new THREE.Mesh(geometry, material);
        sensor.position.set(x, y, z);
        this.scene.add(sensor);
        
        // Add label
        const label = this.createDeviceLabel('Fire Alert', x, y - 0.6, z);

        this.devices[id] = { mesh: sensor, label: label, type: 'sensor' };
    }

    createHeater(id, x, y, z) {
        const geometry = new THREE.BoxGeometry(0.8, 1.2, 0.3);
        const material = new THREE.MeshStandardMaterial({ 
            color: 0x94a3b8,
            metalness: 0.5
        });
        const heater = new THREE.Mesh(geometry, material);
        heater.position.set(x, y, z);
        this.scene.add(heater);

        // Heating element
        const elementGeometry = new THREE.BoxGeometry(0.6, 0.8, 0.1);
        const elementMaterial = new THREE.MeshStandardMaterial({ 
            color: 0xff6b35,
            emissive: 0xff6b35,
            emissiveIntensity: 0
        });
        const element = new THREE.Mesh(elementGeometry, elementMaterial);
        element.position.set(x, y, z + 0.2);
        this.scene.add(element);
        
        // Add label
        const label = this.createDeviceLabel('Heater', x, y - 0.8, z);

        this.devices[id] = { mesh: heater, element: element, label: label, type: 'heater' };
    }

    createFan(id, x, y, z) {
        const geometry = new THREE.CylinderGeometry(0.5, 0.5, 0.2, 32);
        const material = new THREE.MeshStandardMaterial({ 
            color: 0x64748b,
            metalness: 0.6
        });
        const fan = new THREE.Mesh(geometry, material);
        fan.position.set(x, y, z);
        this.scene.add(fan);

        // Fan blades
        const bladeGeometry = new THREE.BoxGeometry(0.8, 0.05, 0.15);
        const bladeMaterial = new THREE.MeshStandardMaterial({ color: 0x475569 });
        const blades = new THREE.Group();
        
        for (let i = 0; i < 4; i++) {
            const blade = new THREE.Mesh(bladeGeometry, bladeMaterial);
            blade.rotation.y = (Math.PI / 2) * i;
            blades.add(blade);
        }
        blades.position.set(x, y - 0.15, z);
        this.scene.add(blades);
        
        // Add label
        const label = this.createDeviceLabel('Fan', x, y - 0.8, z);

        this.devices[id] = { mesh: fan, blades: blades, label: label, type: 'fan', rotation: 0 };
    }

    createWindow(id, x, y, z) {
        const geometry = new THREE.BoxGeometry(0.1, 2, 1.5);
        const material = new THREE.MeshStandardMaterial({ 
            color: 0x3b82f6,
            transparent: true,
            opacity: 0.3,
            metalness: 0.8
        });
        const window = new THREE.Mesh(geometry, material);
        window.position.set(x, y, z);
        this.scene.add(window);
        
        // Add label
        const label = this.createDeviceLabel('Window', x, y + 1.2, z);

        this.devices[id] = { mesh: window, label: label, type: 'window' };
    }

    createAC(id, x, y, z) {
        const geometry = new THREE.BoxGeometry(1.2, 0.4, 0.3);
        const material = new THREE.MeshStandardMaterial({ 
            color: 0xe0e7ff,
            metalness: 0.5
        });
        const ac = new THREE.Mesh(geometry, material);
        ac.position.set(x, y, z);
        this.scene.add(ac);

        // AC particles
        const particlesGeometry = new THREE.BufferGeometry();
        const particlesMaterial = new THREE.PointsMaterial({
            color: 0x06b6d4,
            size: 0.1,
            transparent: true,
            opacity: 0
        });
        const particles = new THREE.Points(particlesGeometry, particlesMaterial);
        particles.position.set(x, y - 0.5, z);
        this.scene.add(particles);
        
        // Add label
        const label = this.createDeviceLabel('AC', x, y - 0.5, z);

        this.devices[id] = { mesh: ac, particles: particles, label: label, type: 'ac' };
    }

    createTV(id, x, y, z) {
        const geometry = new THREE.BoxGeometry(2, 1.2, 0.1);
        const material = new THREE.MeshStandardMaterial({ 
            color: 0x1e293b,
            metalness: 0.8
        });
        const tv = new THREE.Mesh(geometry, material);
        tv.position.set(x, y, z);
        this.scene.add(tv);

        // Screen
        const screenGeometry = new THREE.BoxGeometry(1.8, 1, 0.05);
        const screenMaterial = new THREE.MeshStandardMaterial({ 
            color: 0x000000,
            emissive: 0x3b82f6,
            emissiveIntensity: 0
        });
        const screen = new THREE.Mesh(screenGeometry, screenMaterial);
        screen.position.set(x, y, z + 0.1);
        this.scene.add(screen);
        
        // Add label
        const label = this.createDeviceLabel('TV', x, y - 0.8, z);

        this.devices[id] = { mesh: tv, screen: screen, label: label, type: 'tv' };
    }

    createSoundSystem(id, x, y, z) {
        const geometry = new THREE.BoxGeometry(0.4, 0.6, 0.3);
        const material = new THREE.MeshStandardMaterial({ 
            color: 0x1e293b,
            metalness: 0.6
        });
        
        const speaker1 = new THREE.Mesh(geometry, material);
        speaker1.position.set(x - 0.5, y, z);
        this.scene.add(speaker1);
        
        const speaker2 = new THREE.Mesh(geometry, material);
        speaker2.position.set(x + 0.5, y, z);
        this.scene.add(speaker2);
        
        // Add label
        const label = this.createDeviceLabel('Sound', x, y - 0.5, z);

        this.devices[id] = { mesh: speaker1, mesh2: speaker2, label: label, type: 'sound' };
    }

    createCamera(id, x, y, z) {
        const bodyGeometry = new THREE.CylinderGeometry(0.2, 0.3, 0.4, 16);
        const bodyMaterial = new THREE.MeshStandardMaterial({ 
            color: 0x1e293b,
            metalness: 0.7
        });
        const body = new THREE.Mesh(bodyGeometry, bodyMaterial);
        body.position.set(x, y, z);
        body.rotation.x = Math.PI / 4;
        this.scene.add(body);

        // Lens
        const lensGeometry = new THREE.CircleGeometry(0.15, 32);
        const lensMaterial = new THREE.MeshStandardMaterial({ 
            color: 0x3b82f6,
            emissive: 0x3b82f6,
            emissiveIntensity: 0.5
        });
        const lens = new THREE.Mesh(lensGeometry, lensMaterial);
        lens.position.set(x, y - 0.2, z + 0.2);
        lens.rotation.x = -Math.PI / 4;
        this.scene.add(lens);
        
        // Add label
        const label = this.createDeviceLabel('Camera', x, y - 0.8, z);

        this.devices[id] = { mesh: body, lens: lens, label: label, type: 'camera' };
    }

    createDoor(id, x, y, z) {
        const geometry = new THREE.BoxGeometry(1.5, 3, 0.2);
        const material = new THREE.MeshStandardMaterial({ 
            color: 0x8b5cf6,
            metalness: 0.4
        });
        const door = new THREE.Mesh(geometry, material);
        door.position.set(x, y + 1.5, z);
        
        // Add label
        const label = this.createDeviceLabel('Door', x, y + 3.2, z);
        this.scene.add(door);

        this.devices[id] = { mesh: door, label: label, type: 'door', openAngle: 0 };
    }

    updateDeviceStates() {
        Object.keys(smartHomeData).forEach(roomKey => {
            smartHomeData[roomKey].devices.forEach(device => {
                // Handle special case for out_light (controls 2 lights)
                if (device.id === 'out_light') {
                    const light1 = this.devices['out_light_1'];
                    const light2 = this.devices['out_light_2'];
                    
                    if (light1 && light2) {
                        // Smooth fade in/out
                        const targetIntensity = device.status ? 2 : 0;
                        const targetEmissive = device.status ? 1 : 0;
                        
                        light1.light.intensity += (targetIntensity - light1.light.intensity) * 0.1;
                        light1.mesh.material.emissiveIntensity += (targetEmissive - light1.mesh.material.emissiveIntensity) * 0.1;
                        light2.light.intensity += (targetIntensity - light2.light.intensity) * 0.1;
                        light2.mesh.material.emissiveIntensity += (targetEmissive - light2.mesh.material.emissiveIntensity) * 0.1;
                    }
                    return;
                }
                
                const deviceObj = this.devices[device.id];
                if (!deviceObj) return;

                switch (deviceObj.type) {
                    case 'light':
                        // Check if it's a spot light group
                        if (deviceObj.isSpotGroup && deviceObj.spots) {
                            // Update all spot lights with smooth transition
                            const targetIntensity = device.status ? 0.8 : 0;
                            const targetEmissive = device.status ? 0.6 : 0;
                            
                            deviceObj.spots.forEach(spot => {
                                spot.light.intensity += (targetIntensity - spot.light.intensity) * 0.1;
                                spot.mesh.material.emissiveIntensity += (targetEmissive - spot.mesh.material.emissiveIntensity) * 0.1;
                            });
                        } else if (deviceObj.isMainLight) {
                            // Main light with smooth fade
                            const targetIntensity = device.status ? 2.5 : 0;
                            const targetEmissive = device.status ? 1 : 0;
                            
                            deviceObj.light.intensity += (targetIntensity - deviceObj.light.intensity) * 0.1;
                            deviceObj.mesh.material.emissiveIntensity += (targetEmissive - deviceObj.mesh.material.emissiveIntensity) * 0.1;
                        } else {
                            // Regular light with smooth fade
                            const targetIntensity = device.status ? 1.8 : 0;
                            const targetEmissive = device.status ? 1 : 0;
                            
                            deviceObj.light.intensity += (targetIntensity - deviceObj.light.intensity) * 0.1;
                            deviceObj.mesh.material.emissiveIntensity += (targetEmissive - deviceObj.mesh.material.emissiveIntensity) * 0.1;
                        }
                        break;

                    case 'heater':
                        // Smooth heating effect
                        const targetHeaterEmissive = device.status ? 0.8 : 0;
                        const currentHeaterEmissive = deviceObj.element.material.emissiveIntensity;
                        deviceObj.element.material.emissiveIntensity += (targetHeaterEmissive - currentHeaterEmissive) * 0.05;
                        
                        // Sound effect
                        if (typeof deviceSounds !== 'undefined') {
                            if (device.status && currentHeaterEmissive < 0.1) {
                                deviceSounds.playHeaterSound(device.id);
                            } else if (!device.status && currentHeaterEmissive > 0.7) {
                                deviceSounds.stopSound(device.id);
                            }
                        }
                        break;

                    case 'fan':
                        // Realistic fan acceleration/deceleration
                        if (device.status) {
                            if (!deviceObj.speed) deviceObj.speed = 0;
                            deviceObj.speed = Math.min(deviceObj.speed + 0.01, 0.3); // Accelerate
                            deviceObj.rotation += deviceObj.speed;
                            deviceObj.blades.rotation.y = deviceObj.rotation;
                            
                            // Sound effect
                            if (typeof deviceSounds !== 'undefined' && deviceObj.speed > 0.05) {
                                deviceSounds.playFanSound(device.id, deviceObj.speed);
                            }
                        } else {
                            if (deviceObj.speed > 0) {
                                deviceObj.speed = Math.max(deviceObj.speed - 0.005, 0); // Decelerate
                                deviceObj.rotation += deviceObj.speed;
                                deviceObj.blades.rotation.y = deviceObj.rotation;
                                
                                // Stop sound when fully stopped
                                if (typeof deviceSounds !== 'undefined' && deviceObj.speed < 0.01) {
                                    deviceSounds.stopSound(device.id);
                                }
                            }
                        }
                        break;

                    case 'window':
                        // Smooth window opening/closing
                        const targetOpacity = device.status ? 0.8 : 0.3;
                        const currentOpacity = deviceObj.mesh.material.opacity;
                        const prevOpacity = deviceObj.prevOpacity || currentOpacity;
                        deviceObj.mesh.material.opacity += (targetOpacity - currentOpacity) * 0.05;
                        
                        // Sound effect on state change
                        if (typeof deviceSounds !== 'undefined') {
                            if (Math.abs(prevOpacity - currentOpacity) > 0.01 && Math.abs(targetOpacity - currentOpacity) > 0.1) {
                                if (!deviceObj.soundPlayed) {
                                    deviceSounds.playWindowSound(device.status);
                                    deviceObj.soundPlayed = true;
                                }
                            } else if (Math.abs(targetOpacity - currentOpacity) < 0.05) {
                                deviceObj.soundPlayed = false;
                            }
                        }
                        deviceObj.prevOpacity = currentOpacity;
                        break;

                    case 'ac':
                        // Smooth AC particles fade
                        const targetACOpacity = device.status ? 0.6 : 0;
                        const currentACOpacity = deviceObj.particles.material.opacity;
                        deviceObj.particles.material.opacity += (targetACOpacity - currentACOpacity) * 0.05;
                        
                        // Sound effect
                        if (typeof deviceSounds !== 'undefined') {
                            if (device.status && currentACOpacity < 0.1) {
                                deviceSounds.playACSound(device.id);
                            } else if (!device.status && currentACOpacity > 0.5) {
                                deviceSounds.stopSound(device.id);
                            }
                        }
                        break;

                    case 'tv':
                        // Smooth TV screen fade
                        const targetTVEmissive = device.status ? 0.5 : 0;
                        const currentTVEmissive = deviceObj.screen.material.emissiveIntensity;
                        deviceObj.screen.material.emissiveIntensity += (targetTVEmissive - currentTVEmissive) * 0.08;
                        
                        // Sound effect
                        if (typeof deviceSounds !== 'undefined') {
                            if (device.status && currentTVEmissive < 0.1) {
                                deviceSounds.playTVSound(device.id);
                            } else if (!device.status && currentTVEmissive > 0.4) {
                                deviceSounds.stopSound(device.id);
                            }
                        }
                        break;
                    
                    case 'sound':
                        // Sound system
                        if (typeof deviceSounds !== 'undefined') {
                            if (device.status && !deviceObj.soundActive) {
                                deviceSounds.playSoundSystem(device.id);
                                deviceObj.soundActive = true;
                            } else if (!device.status && deviceObj.soundActive) {
                                deviceSounds.stopSound(device.id);
                                deviceObj.soundActive = false;
                            }
                        }
                        break;
                    
                    case 'sensor':
                        // Fire alert sensor
                        if (device.id.includes('fire')) {
                            const targetSensorEmissive = device.status ? 1 : 0;
                            const currentSensorEmissive = deviceObj.mesh.material.emissiveIntensity;
                            deviceObj.mesh.material.emissiveIntensity += (targetSensorEmissive - currentSensorEmissive) * 0.1;
                            
                            // Track previous state
                            if (!deviceObj.prevStatus) deviceObj.prevStatus = false;
                            
                            // Fire alarm sound - ONLY during fire emergency
                            if (typeof deviceSounds !== 'undefined' && typeof window !== 'undefined') {
                                const isFireEmergency = window.fireEmergencyActive === true;
                                
                                // Start alarm immediately when sensor turns ON during fire emergency
                                if (device.status && isFireEmergency && !deviceObj.prevStatus) {
                                    deviceSounds.playFireAlarm(device.id);
                                    console.log(`🚨 Fire alarm started for ${device.id}`);
                                } 
                                // Stop alarm immediately when sensor turns OFF
                                else if (!device.status && deviceObj.prevStatus) {
                                    deviceSounds.stopSound(device.id);
                                    console.log(`✅ Fire alarm stopped for ${device.id}`);
                                }
                                // Stop alarm if fire emergency ended
                                else if (!isFireEmergency && deviceObj.prevStatus) {
                                    deviceSounds.stopSound(device.id);
                                    console.log(`✅ Fire alarm stopped (emergency ended) for ${device.id}`);
                                }
                            }
                            
                            // Update previous status
                            deviceObj.prevStatus = device.status;
                        }
                        break;
                    
                    case 'door':
                        // Door opening/closing
                        const targetAngle = device.status ? Math.PI / 2 : 0;
                        const currentAngle = deviceObj.openAngle || 0;
                        deviceObj.openAngle += (targetAngle - currentAngle) * 0.05;
                        deviceObj.mesh.rotation.y = deviceObj.openAngle;
                        
                        // Sound effect on state change
                        if (typeof deviceSounds !== 'undefined') {
                            if (Math.abs(targetAngle - currentAngle) > 0.1 && !deviceObj.doorSoundPlayed) {
                                deviceSounds.playDoorSound(device.status);
                                deviceObj.doorSoundPlayed = true;
                            } else if (Math.abs(targetAngle - currentAngle) < 0.05) {
                                deviceObj.doorSoundPlayed = false;
                            }
                        }
                        break;

                    case 'sound':
                        if (device.status) {
                            const scale = 1 + Math.sin(Date.now() * 0.01) * 0.1;
                            deviceObj.mesh.scale.set(1, scale, 1);
                            if (deviceObj.mesh2) deviceObj.mesh2.scale.set(1, scale, 1);
                        } else {
                            deviceObj.mesh.scale.set(1, 1, 1);
                            if (deviceObj.mesh2) deviceObj.mesh2.scale.set(1, 1, 1);
                        }
                        break;

                    case 'door':
                        if (device.status) {
                            deviceObj.openAngle = Math.min(deviceObj.openAngle + 0.02, Math.PI / 2);
                        } else {
                            deviceObj.openAngle = Math.max(deviceObj.openAngle - 0.02, 0);
                        }
                        deviceObj.mesh.rotation.y = deviceObj.openAngle;
                        break;
                }
            });
        });

        // Update fire sensors
        Object.keys(this.devices).forEach(id => {
            const device = this.devices[id];
            if (device.type === 'sensor') {
                if (simulation.smokeDetected) {
                    device.mesh.material.emissiveIntensity = 1;
                } else {
                    device.mesh.material.emissiveIntensity = 0;
                }
            }
        });
    }

    createSensorsPanel() {
        this.sensors = [
            { id: 'temp', name: 'Temperature', unit: '°C', value: 25, location: 'Living Area', type: 'temperature' },
            { id: 'humidity', name: 'Humidity', unit: '%', value: 45, location: 'Bathroom', type: 'humidity' },
            { id: 'motion', name: 'Motion Sensor', unit: '', value: 'No Motion', location: 'Corridors', type: 'motion' },
            { id: 'smoke', name: 'Smoke Detector', unit: '', value: 'Clear', location: 'Kitchen', type: 'smoke' },
            { id: 'door', name: 'Door Sensor', unit: '', value: 'Closed', location: 'Main Entrance', type: 'door' },
            { id: 'light_level', name: 'Light Level', unit: 'lux', value: 320, location: 'Reception', type: 'light' },
            { id: 'energy', name: 'Power Usage', unit: 'kW', value: 0, location: 'Main Panel', type: 'energy' }
        ];

        this.renderSensors();
    }

    renderSensors() {
        const container = document.getElementById('sensors-grid');
        if (!container) return;
        
        container.innerHTML = '';

        this.sensors.forEach(sensor => {
            const card = document.createElement('div');
            card.className = 'sensor-card';
            
            const isActive = this.getSensorStatus(sensor);
            const displayValue = this.getSensorDisplayValue(sensor);
            
            card.innerHTML = `
                <div class="sensor-header">
                    <span class="sensor-name">${sensor.name}</span>
                    <span class="sensor-status ${isActive ? 'active' : 'inactive'}">
                        ${isActive ? 'Active' : 'Inactive'}
                    </span>
                </div>
                <div class="sensor-value">${displayValue}</div>
                <div class="sensor-location">${sensor.location}</div>
            `;
            
            container.appendChild(card);
        });
    }

    getSensorStatus(sensor) {
        if (sensor.type === 'motion') return simulation.motionDetected;
        if (sensor.type === 'smoke') return simulation.smokeDetected;
        return true;
    }

    getSensorDisplayValue(sensor) {
        if (sensor.type === 'temperature') {
            return `${simulation.temperature.toFixed(1)}${sensor.unit}`;
        }
        if (sensor.type === 'motion') {
            return simulation.motionDetected ? 'Motion Detected' : 'No Motion';
        }
        if (sensor.type === 'smoke') {
            return simulation.smokeDetected ? 'SMOKE DETECTED!' : 'Clear';
        }
        if (sensor.type === 'energy') {
            return `${simulation.calculateEnergyUsage()} ${sensor.unit}`;
        }
        if (sensor.type === 'humidity') {
            const humidity = 40 + Math.random() * 20;
            return `${humidity.toFixed(0)}${sensor.unit}`;
        }
        if (sensor.type === 'light') {
            const hour = new Date().getHours();
            const lightLevel = hour >= 6 && hour <= 18 ? 300 + Math.random() * 200 : 50 + Math.random() * 100;
            return `${lightLevel.toFixed(0)} ${sensor.unit}`;
        }
        if (sensor.type === 'door') {
            return Math.random() > 0.95 ? 'Open' : 'Closed';
        }
        return `${sensor.value}${sensor.unit}`;
    }

    startSensorUpdates() {
        setInterval(() => {
            this.renderSensors();
        }, 1000);
    }

    onWindowResize() {
        if (!this.container || !this.container.clientWidth) return;
        
        const width = this.container.clientWidth;
        const height = this.container.clientHeight;
        
        this.camera.aspect = width / height;
        this.camera.updateProjectionMatrix();
        this.renderer.setSize(width, height);
    }

    animate() {
        requestAnimationFrame(() => this.animate());
        
        if (this.controls) this.controls.update();
        if (this.scene && this.camera && this.renderer) {
            this.updateDeviceStates();
            this.renderer.render(this.scene, this.camera);
        }
    }
}

// Make Apartment3D available globally
window.Apartment3D = Apartment3D;
