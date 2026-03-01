// Main Application Logic
// Global 3D apartment instance
let apartment3D = null;

class SmartHomeApp {
    constructor() {
        this.currentFilter = 'all';
        this.currentView = 'control';
        this.init();
    }

    init() {
        this.renderRooms();
        this.setupNavigation();
        this.setupViewSwitching();
        this.updateTime();
        this.startSimulation();
        
        setInterval(() => this.updateTime(), 1000);
    }

    // Setup view switching
    setupViewSwitching() {
        const tabButtons = document.querySelectorAll('.tab-btn');
        
        tabButtons.forEach(btn => {
            btn.addEventListener('click', () => {
                const view = btn.getAttribute('data-view');
                this.switchView(view);
                
                tabButtons.forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
            });
        });
    }

    // Switch between views
    switchView(view) {
        this.currentView = view;
        
        document.querySelectorAll('.view-container').forEach(container => {
            container.classList.remove('active');
        });
        
        const viewContainer = document.getElementById(`${view}-view`);
        if (viewContainer) {
            viewContainer.classList.add('active');
        }
        
        // Initialize 3D apartment if switching to simulation view
        if (view === 'simulation') {
            if (!apartment3D) {
                // Wait for container to be visible
                setTimeout(() => {
                    apartment3D = new Apartment3D();
                }, 100);
            } else {
                // Trigger resize to fix canvas
                setTimeout(() => {
                    if (apartment3D && apartment3D.onWindowResize) {
                        apartment3D.onWindowResize();
                    }
                }, 100);
            }
        }
    }

    // Render all rooms
    renderRooms() {
        const container = document.getElementById('rooms-container');
        if (!container) {
            console.error('rooms-container not found!');
            return;
        }
        
        container.innerHTML = '';
        console.log('Rendering rooms...', Object.keys(smartHomeData).length, 'rooms');

        Object.keys(smartHomeData).forEach(roomKey => {
            const room = smartHomeData[roomKey];
            console.log('Rendering room:', room.name, 'with', room.devices.length, 'devices');
            const roomCard = this.createRoomCard(roomKey, room);
            container.appendChild(roomCard);
        });
        
        console.log('Rooms rendered successfully!');
    }

    // Create room card
    createRoomCard(roomKey, room) {
        const card = document.createElement('div');
        card.className = 'room-card';
        card.dataset.room = roomKey;

        const devicesHTML = room.devices.map(device => 
            this.createDeviceHTML(roomKey, device)
        ).join('');

        card.innerHTML = `
            <div class="room-header">
                <h2 class="room-title">${room.name}</h2>
                <span class="room-icon"></span>
            </div>
            <div class="devices-list">
                ${devicesHTML}
            </div>
        `;

        return card;
    }

    // Create device HTML
    createDeviceHTML(roomKey, device) {
        const statusText = device.status ? 'ON' : 'OFF';
        const activeClass = device.status ? 'active' : '';
        
        // Icon SVG paths for each device type
        const iconPaths = {
            light: '<path d="M12,6A6,6 0 0,1 18,12C18,14.22 16.79,16.16 15,17.2V19A1,1 0 0,1 14,20H10A1,1 0 0,1 9,19V17.2C7.21,16.16 6,14.22 6,12A6,6 0 0,1 12,6M14,21V22A1,1 0 0,1 13,23H11A1,1 0 0,1 10,22V21H14M20,11H23V13H20V11M1,11H4V13H1V11M13,1V4H11V1H13M4.92,3.5L7.05,5.64L5.63,7.05L3.5,4.93L4.92,3.5M16.95,5.63L19.07,3.5L20.5,4.93L18.37,7.05L16.95,5.63Z"/>',
            ac: '<path d="M6.59,0.66C8.93,1.07 10.62,3.61 10.62,6.5C10.62,9.39 8.93,11.93 6.59,12.34V13.5C8.93,13.91 10.62,16.45 10.62,19.34C10.62,22.23 8.93,24.77 6.59,25.18V27H5.59V25.18C3.25,24.77 1.56,22.23 1.56,19.34C1.56,16.45 3.25,13.91 5.59,13.5V12.34C3.25,11.93 1.56,9.39 1.56,6.5C1.56,3.61 3.25,1.07 5.59,0.66V0H6.59V0.66M13.5,7V9H22.5V7H13.5M13.5,18V20H22.5V18H13.5Z"/>',
            fan: '<path d="M12,11A1,1 0 0,0 11,12A1,1 0 0,0 12,13A1,1 0 0,0 13,12A1,1 0 0,0 12,11M12.5,2C17,2 17.11,5.57 14.75,6.75C13.76,7.24 13.32,8.29 13.13,9.22C13.61,9.42 14.03,9.73 14.35,10.13C18.05,8.13 22.03,8.92 22.03,12.5C22.03,17 18.46,17.1 17.28,14.73C16.78,13.74 15.72,13.3 14.79,13.11C14.59,13.59 14.28,14 13.88,14.34C15.87,18.03 15.08,22 11.5,22C7,22 6.91,18.42 9.27,17.24C10.25,16.75 10.69,15.71 10.89,14.79C10.4,14.59 9.97,14.27 9.65,13.87C5.96,15.85 2,15.07 2,11.5C2,7 5.56,6.89 6.74,9.26C7.24,10.25 8.29,10.68 9.22,10.87C9.41,10.39 9.73,9.97 10.14,9.65C8.15,5.96 8.94,2 12.5,2Z"/>',
            window: '<path d="M21,20V2H3V20H1V23H23V20M19,4V11H13V4M5,4H11V11H5M5,20V13H11V20M13,20V13H19V20"/>',
            door: '<path d="M8,3C6.89,3 6,3.89 6,5V21H18V5C18,3.89 17.11,3 16,3H8M8,5H16V19H8V5M13,11V13H15V11H13Z"/>',
            camera: '<path d="M4,4H7L9,2H15L17,4H20A2,2 0 0,1 22,6V18A2,2 0 0,1 20,20H4A2,2 0 0,1 2,18V6A2,2 0 0,1 4,4M12,7A5,5 0 0,0 7,12A5,5 0 0,0 12,17A5,5 0 0,0 17,12A5,5 0 0,0 12,7M12,9A3,3 0 0,1 15,12A3,3 0 0,1 12,15A3,3 0 0,1 9,12A3,3 0 0,1 12,9Z"/>',
            tv: '<path d="M21,17H3V5H21M21,3H3A2,2 0 0,0 1,5V17A2,2 0 0,0 3,19H8V21H16V19H21A2,2 0 0,0 23,17V5A2,2 0 0,0 21,3Z"/>',
            sound: '<path d="M14,3.23V5.29C16.89,6.15 19,8.83 19,12C19,15.17 16.89,17.84 14,18.7V20.77C18,19.86 21,16.28 21,12C21,7.72 18,4.14 14,3.23M16.5,12C16.5,10.23 15.5,8.71 14,7.97V16C15.5,15.29 16.5,13.76 16.5,12M3,9V15H7L12,20V4L7,9H3Z"/>',
            sensor: '<path d="M17.66,11.2C17.43,10.9 17.15,10.64 16.89,10.38C16.22,9.78 15.46,9.35 14.82,8.72C13.33,7.26 13,4.85 13.95,3C13,3.23 12.17,3.75 11.46,4.32C8.87,6.4 7.85,10.07 9.07,13.22C9.11,13.32 9.15,13.42 9.15,13.55C9.15,13.77 9,13.97 8.8,14.05C8.57,14.15 8.33,14.09 8.14,13.93C8.08,13.88 8.04,13.83 8,13.76C6.87,12.33 6.69,10.28 7.45,8.64C5.78,10 4.87,12.3 5,14.47C5.06,14.97 5.12,15.47 5.29,15.97C5.43,16.57 5.7,17.17 6,17.7C7.08,19.43 8.95,20.67 10.96,20.92C13.1,21.19 15.39,20.8 17.03,19.32C18.86,17.66 19.5,15 18.56,12.72L18.43,12.46C18.22,12 17.66,11.2 17.66,11.2M14.5,17.5C14.22,17.74 13.76,18 13.4,18.1C12.28,18.5 11.16,17.94 10.5,17.28C11.69,17 12.4,16.12 12.61,15.23C12.78,14.43 12.46,13.77 12.33,13C12.21,12.26 12.23,11.63 12.5,10.94C12.69,11.32 12.89,11.7 13.13,12C13.9,13 15.11,13.44 15.37,14.8C15.41,14.94 15.43,15.08 15.43,15.23C15.46,16.05 15.1,16.95 14.5,17.5H14.5Z"/>',
            heater: '<path d="M17,13A5,5 0 0,0 12,8A5,5 0 0,0 7,13A5,5 0 0,0 12,18A5,5 0 0,0 17,13M12,2A2,2 0 0,1 14,4C14,4.74 13.6,5.39 13,5.73V7H11V5.73C10.4,5.39 10,4.74 10,4A2,2 0 0,1 12,2Z"/>'
        };
        
        const iconPath = iconPaths[device.type] || iconPaths.light;
        
        return `
            <div class="device-item ${activeClass}" 
                 data-device-id="${device.id}" 
                 data-type="${device.type}"
                 onclick="app.toggleDevice('${roomKey}', '${device.id}')">
                <div class="ripple-container">
                    <div class="ripple"></div>
                </div>
                <div class="device-info">
                    <div class="device-icon">
                        <svg viewBox="0 0 24 24" width="24" height="24">
                            ${iconPath}
                        </svg>
                    </div>
                    <div class="device-name">${device.name}</div>
                    <div class="device-status">${statusText}</div>
                </div>
            </div>
        `;
    }

    // Toggle device
    async toggleDevice(roomKey, deviceId) {
        const room = smartHomeData[roomKey];
        const device = room.devices.find(d => d.id === deviceId);
        
        if (device) {
            const newStatus = !device.status;
            const deviceElement = document.querySelector(`[data-device-id="${deviceId}"]`);
            
            // Trigger ripple effect
            if (deviceElement) {
                const ripple = deviceElement.querySelector('.ripple');
                if (ripple) {
                    // Get click position
                    const rect = deviceElement.getBoundingClientRect();
                    const size = Math.max(rect.width, rect.height);
                    const x = rect.width / 2;
                    const y = rect.height / 2;
                    
                    ripple.style.width = ripple.style.height = size + 'px';
                    ripple.style.left = x - size / 2 + 'px';
                    ripple.style.top = y - size / 2 + 'px';
                    
                    // Remove and re-add animation
                    ripple.style.animation = 'none';
                    setTimeout(() => {
                        ripple.style.animation = 'ripple-animation 0.6s ease-out';
                    }, 10);
                }
            }
            
            // Send to AI backend first
            if (typeof aiClient !== 'undefined') {
                const action = newStatus ? 'on' : 'off';
                const result = await aiClient.controlDevice(deviceId, action);
                
                if (result.success) {
                    console.log(`Device ${deviceId} controlled via backend:`, result);
                } else {
                    console.warn(`Failed to control device ${deviceId} via backend, updating locally`);
                }
            }
            
            // Update local state
            device.status = newStatus;
            
            // IMMEDIATELY stop fire alarm sound if turning off fire sensor
            if (deviceId.includes('fire') && !newStatus && typeof deviceSounds !== 'undefined') {
                deviceSounds.stopSound(deviceId);
            }
            
            simulation.logEvent(`${device.name} in ${room.name} turned ${device.status ? 'ON' : 'OFF'}`);
            
            this.applyAIRules(roomKey, device);
            
            // Update UI immediately
            if (deviceElement) {
                if (device.status) {
                    deviceElement.classList.add('active');
                } else {
                    deviceElement.classList.remove('active');
                }
                const statusElement = deviceElement.querySelector('.device-status');
                if (statusElement) {
                    statusElement.textContent = device.status ? 'ON' : 'OFF';
                }
            }
            
            // Update 3D view if active
            if (apartment3D) {
                apartment3D.updateDeviceStates();
            }
        }
    }

    // Apply AI rules
    applyAIRules(roomKey, device) {
        if (device.type === 'ac' && device.status) {
            simulation.addAISuggestion("AC is on. Consider closing windows for better efficiency.");
        }

        if (device.type === 'light' && device.status) {
            const hour = new Date().getHours();
            if (hour >= 6 && hour <= 18) {
                simulation.addAISuggestion("It's daytime. Natural light might be sufficient.");
            }
        }

        if (device.type === 'tv' && device.status) {
            const room = smartHomeData[roomKey];
            const soundSystem = room.devices.find(d => d.type === 'sound');
            if (soundSystem && !soundSystem.status) {
                simulation.addAISuggestion("TV is on. Would you like to turn on the sound system?");
            }
        }

        if (device.type === 'heater' && device.status) {
            setTimeout(() => {
                if (device.status) {
                    simulation.addAlert("Water heater has been on for a while. Consider turning it off.", "warning");
                }
            }, 30000);
        }
    }

    // Setup navigation
    setupNavigation() {
        const navButtons = document.querySelectorAll('.nav-btn');
        
        navButtons.forEach(btn => {
            btn.addEventListener('click', () => {
                navButtons.forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                
                const room = btn.dataset.room;
                this.applyFilter(room);
            });
        });
    }

    // Apply room filter
    applyFilter(room) {
        this.currentFilter = room;
        const cards = document.querySelectorAll('.room-card');
        
        cards.forEach(card => {
            if (room === 'all' || card.dataset.room === room) {
                card.classList.remove('hidden');
            } else {
                card.classList.add('hidden');
            }
        });
    }

    // Update time
    updateTime() {
        const now = new Date();
        const timeString = now.toLocaleTimeString('en-US', { 
            hour: '2-digit', 
            minute: '2-digit',
            second: '2-digit'
        });
        const dateString = now.toLocaleDateString('en-US', {
            weekday: 'short',
            year: 'numeric',
            month: 'short',
            day: 'numeric'
        });
        
        document.getElementById('current-time').textContent = `${dateString} ${timeString}`;
    }

    // Start simulation
    startSimulation() {
        simulation.startSimulations();
        
        // Removed automatic device toggling - user has full manual control
        // Auto Mode in AI tab handles automation when enabled
    }
}

// Initialize app when DOM is ready
let app;
document.addEventListener('DOMContentLoaded', () => {
    app = new SmartHomeApp();
    
    // Show Emma voice control notification after 3 seconds
    setTimeout(() => {
        showNotification('🎤 Emma is Ready!', 'Say "Hey Emma" to start giving voice commands', 'info');
    }, 3000);
});

// Notification helper function
function showNotification(title, message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `voice-notification ${type}`;
    notification.innerHTML = `
        <div class="notification-content">
            <strong>${title}</strong>
            <p>${message}</p>
        </div>
    `;
    
    document.body.appendChild(notification);
    
    // Animate in
    setTimeout(() => notification.classList.add('show'), 100);
    
    // Remove after 5 seconds
    setTimeout(() => {
        notification.classList.remove('show');
        setTimeout(() => notification.remove(), 300);
    }, 5000);
}