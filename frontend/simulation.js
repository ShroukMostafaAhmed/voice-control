// Simulation Engine
class SmartHomeSimulation {
    constructor() {
        this.temperature = 25;
        this.motionDetected = false;
        this.smokeDetected = false;
        this.alerts = [];
        this.aiSuggestions = [];
        this.eventLog = [];
    }

    // Simulate temperature changes
    simulateTemperature() {
        setInterval(() => {
            const change = (Math.random() - 0.5) * 2;
            this.temperature = Math.max(15, Math.min(40, this.temperature + change));
            
            // AI Rule: If temperature > 28 and someone present, suggest AC
            if (this.temperature > 28 && this.motionDetected) {
                this.addAISuggestion("Temperature is high. Consider turning on AC in occupied rooms.");
            }
            
            // AI Rule: If temperature < 18, suggest heater
            if (this.temperature < 18) {
                this.addAISuggestion("Temperature is low. Consider turning on water heater.");
            }
        }, 5000);
    }

    // Simulate motion detection
    simulateMotion() {
        setInterval(() => {
            this.motionDetected = Math.random() > 0.5;
            
            // AI Rule: No motion for extended period, suggest turning off lights
            if (!this.motionDetected) {
                setTimeout(() => {
                    if (!this.motionDetected) {
                        this.addAISuggestion("No motion detected. Turn off lights to save energy.");
                    }
                }, 10000);
            }
        }, 15000);
    }

    // Simulate fire/smoke detection
    simulateFireDetection() {
        setInterval(() => {
            const fireChance = Math.random();
            
            if (fireChance > 0.98) {
                this.smokeDetected = true;
                this.triggerFireAlert();
                
                setTimeout(() => {
                    this.smokeDetected = false;
                    this.clearFireAlert();
                }, 30000);
            }
        }, 10000);
    }

    // Trigger fire alert
    triggerFireAlert() {
        this.addAlert("FIRE DETECTED! Opening windows and alerting authorities.", "danger");
        
        // AI Action: Open all windows
        Object.keys(smartHomeData).forEach(roomKey => {
            smartHomeData[roomKey].devices.forEach(device => {
                if (device.type === 'window') {
                    device.status = true;
                }
            });
        });
        
        this.logEvent("Fire detected - Emergency protocol activated");
    }

    // Clear fire alert
    clearFireAlert() {
        this.addAlert("Fire alert cleared. System returning to normal.", "safe");
        this.logEvent("Fire alert cleared");
    }

    // Add alert
    addAlert(message, type = "safe") {
        this.alerts.unshift({ message, type, timestamp: new Date() });
        if (this.alerts.length > 5) {
            this.alerts.pop();
        }
        this.updateAlertsUI();
    }

    // Add AI suggestion
    addAISuggestion(message) {
        if (!this.aiSuggestions.some(s => s.message === message)) {
            this.aiSuggestions.unshift({ message, timestamp: new Date() });
            if (this.aiSuggestions.length > 3) {
                this.aiSuggestions.pop();
            }
            this.updateSuggestionsUI();
        }
    }

    // Log event
    logEvent(event) {
        this.eventLog.unshift({
            event,
            timestamp: new Date()
        });
        if (this.eventLog.length > 50) {
            this.eventLog.pop();
        }
    }

    // Update alerts UI
    updateAlertsUI() {
        const container = document.getElementById('alerts-container');
        container.innerHTML = '';
        
        if (this.alerts.length === 0) {
            container.innerHTML = `
                <div class="alert-item safe">
                    <span class="alert-icon">✓</span>
                    <span>All systems normal</span>
                </div>
            `;
        } else {
            this.alerts.forEach(alert => {
                const alertDiv = document.createElement('div');
                alertDiv.className = `alert-item ${alert.type}`;
                alertDiv.innerHTML = `
                    <span class="alert-icon">${alert.type === 'danger' ? '!' : alert.type === 'warning' ? '!' : '✓'}</span>
                    <span>${alert.message}</span>
                `;
                container.appendChild(alertDiv);
            });
        }
    }

    // Update suggestions UI
    updateSuggestionsUI() {
        const container = document.getElementById('ai-suggestions');
        container.innerHTML = '';
        
        if (this.aiSuggestions.length === 0) {
            container.innerHTML = `
                <div class="suggestion-item">
                    <p>System is optimized. No suggestions at the moment.</p>
                </div>
            `;
        } else {
            this.aiSuggestions.forEach(suggestion => {
                const suggestionDiv = document.createElement('div');
                suggestionDiv.className = 'suggestion-item';
                suggestionDiv.innerHTML = `<p>${suggestion.message}</p>`;
                container.appendChild(suggestionDiv);
            });
        }
    }

    // Simulate energy optimization
    simulateEnergyOptimization() {
        setInterval(() => {
            const activeDevices = this.getActiveDevicesCount();
            
            if (activeDevices > 10) {
                this.addAISuggestion("High energy usage detected. Consider turning off unused devices.");
            }
            
            const tips = [
                "Turn off lights in empty rooms to save 12% energy",
                "Set AC to 24°C for optimal energy efficiency",
                "Enable night mode to reduce power consumption",
                "Unplug devices on standby to save energy"
            ];
            
            if (Math.random() > 0.95) {
                const randomTip = tips[Math.floor(Math.random() * tips.length)];
                this.addAISuggestion(randomTip);
            }
        }, 20000);
    }

    // Get active devices count
    getActiveDevicesCount() {
        let count = 0;
        Object.keys(smartHomeData).forEach(roomKey => {
            smartHomeData[roomKey].devices.forEach(device => {
                if (device.status) count++;
            });
        });
        return count;
    }

    // Calculate total energy usage
    calculateEnergyUsage() {
        const deviceEnergy = {
            light: 60,
            sensor: 5,
            heater: 2000,
            fan: 75,
            window: 10,
            sound: 50,
            camera: 15,
            door: 20,
            ac: 1500,
            tv: 150
        };
        
        let totalEnergy = 0;
        Object.keys(smartHomeData).forEach(roomKey => {
            smartHomeData[roomKey].devices.forEach(device => {
                if (device.status) {
                    totalEnergy += deviceEnergy[device.type] || 0;
                }
            });
        });
        return (totalEnergy / 1000).toFixed(2);
    }

    // Start all simulations
    startSimulations() {
        this.simulateTemperature();
        this.simulateMotion();
        this.simulateFireDetection();
        this.simulateEnergyOptimization();
        
        setInterval(() => {
            document.getElementById('active-devices').textContent = this.getActiveDevicesCount();
            document.getElementById('energy-usage').textContent = this.calculateEnergyUsage() + ' kW';
        }, 1000);
    }
}

// Initialize simulation
const simulation = new SmartHomeSimulation();
