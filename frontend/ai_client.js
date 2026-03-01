// AI System Client

class AIClient {
    constructor(baseURL = 'http://localhost:8090') {
        this.baseURL = baseURL;
        this.chatMessages = [];
        this.autoModePolling = null;
    }

    async get(endpoint) {
        try {
            const response = await fetch(`${this.baseURL}${endpoint}`);
            return await response.json();
        } catch (error) {
            console.error(`AI API error: ${endpoint}`, error);
            return { success: false, error: error.message };
        }
    }

    async post(endpoint, body = {}) {
        try {
            const response = await fetch(`${this.baseURL}${endpoint}`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(body)
            });
            return await response.json();
        } catch (error) {
            console.error(`AI API error: ${endpoint}`, error);
            return { success: false, error: error.message };
        }
    }

    // AI Commands
    async sendCommand(command) {
        const useMistral = document.getElementById('use-mistral-toggle')?.checked ?? true;
        const result = await this.post('/api/ai/command', { 
            command,
            use_mistral: useMistral
        });
        
        if (result.success) {
            await this.syncDeviceStates();
        }
        
        return result;
    }
    
    async syncDeviceStates() {
        const devicesResult = await this.getDevices();
        if (!devicesResult.success) {
            console.log('Failed to sync device states:', devicesResult);
            return;
        }
        
        console.log('Syncing device states from AI backend...', devicesResult.data.length, 'devices');
        
        let updatedCount = 0;
        devicesResult.data.forEach(device => {
            const roomKey = this.getRoomKeyFromName(device.room);
            if (!roomKey || !smartHomeData[roomKey]) return;
            
            const frontendDevice = smartHomeData[roomKey].devices.find(d => 
                d.id === device.device_id
            );
            
            if (frontendDevice) {
                const oldStatus = frontendDevice.status;
                frontendDevice.status = device.state === 1;
                if (oldStatus !== frontendDevice.status) {
                    console.log(`✓ Updated ${device.device_id}: ${oldStatus ? 'ON' : 'OFF'} -> ${frontendDevice.status ? 'ON' : 'OFF'}`);
                    updatedCount++;
                }
            }
        });
        
        if (updatedCount > 0) {
            console.log(`✓ Sync complete: ${updatedCount} devices updated`);
            
            // Update 3D simulation
            if (typeof apartment3D !== 'undefined' && apartment3D) {
                apartment3D.updateDeviceStates();
            }
            
            // Update Control Panel
            if (typeof app !== 'undefined' && app) {
                app.renderRooms();
                app.applyFilter(app.currentFilter);
            }
        } else {
            console.log('Sync complete: No changes');
        }
    }
    
    getRoomKeyFromName(roomName) {
        const roomMap = {
            'bathroom': 'bathroom',
            'corridors': 'corridors',
            'reception': 'reception',
            'outdoor': 'outdoor',
            'room1': 'room1',
            'kitchen': 'kitchen',
            'room2': 'room2'
        };
        return roomMap[roomName.toLowerCase()];
    }

    async analyzeEnvironment() {
        return await this.get('/api/ai/analyze');
    }

    async executeAIDecisions() {
        const result = await this.post('/api/ai/execute');
        
        if (result.success && result.executed > 0) {
            await this.syncDeviceStates();
        }
        
        return result;
    }

    async getSuggestions() {
        return await this.get('/api/ai/suggestions');
    }

    async getStatistics() {
        return await this.get('/api/ai/statistics');
    }

    async getEnvironment() {
        return await this.get('/api/environment');
    }

    async getDevices() {
        return await this.get('/api/devices');
    }

    async controlDevice(deviceId, action) {
        return await this.post('/api/devices/control', { device_id: deviceId, action });
    }
    
    async toggleAutoMode() {
        return await this.post('/api/ai/auto-mode/toggle');
    }
    
    async getAutoModeStatus() {
        return await this.get('/api/ai/auto-mode/status');
    }

    // Chat UI
    addMessage(content, isUser = false) {
        const container = document.getElementById('ai-chat-messages');
        if (!container) return;

        const messageDiv = document.createElement('div');
        messageDiv.className = `ai-message ${isUser ? 'ai-message-user' : 'ai-message-assistant'}`;
        
        messageDiv.innerHTML = `
            <div class="ai-avatar">${isUser ? 'You' : 'Emma'}</div>
            <div class="ai-message-content">
                <p>${content}</p>
            </div>
        `;
        
        container.appendChild(messageDiv);
        container.scrollTop = container.scrollHeight;
        
        this.chatMessages.push({ content, isUser, timestamp: new Date() });
    }

    async updateEnvironment() {
        const result = await this.getEnvironment();
        if (!result.success) return;

        const env = result.data;
        const container = document.getElementById('ai-environment');
        if (!container) return;

        container.innerHTML = `
            <div class="env-item">
                <span class="env-label">Temperature</span>
                <span class="env-value">${env.temperature}°C</span>
            </div>
            <div class="env-item">
                <span class="env-label">Humidity</span>
                <span class="env-value">${env.humidity}%</span>
            </div>
            <div class="env-item">
                <span class="env-label">Motion</span>
                <span class="env-value">${env.motion ? 'Detected' : 'None'}</span>
            </div>
            <div class="env-item">
                <span class="env-label">Light Level</span>
                <span class="env-value">${env.light_level} lux</span>
            </div>
        `;
    }

    async updateSuggestions() {
        const result = await this.getSuggestions();
        if (!result.success) return;

        const container = document.getElementById('ai-suggestions-list');
        if (!container) return;

        if (result.suggestions.length === 0) {
            container.innerHTML = '<div class="ai-suggestion">No suggestions at the moment</div>';
            return;
        }

        container.innerHTML = result.suggestions.map(s => 
            `<div class="ai-suggestion">${s}</div>`
        ).join('');
    }

    async updateStatistics() {
        const result = await this.getStatistics();
        if (!result.success) return;

        const stats = result.data;
        const container = document.getElementById('ai-stats');
        if (!container) return;

        container.innerHTML = `
            <div class="stat-item">
                <span class="stat-label">Total Decisions</span>
                <span class="stat-value">${stats.total_decisions}</span>
            </div>
            <div class="stat-item">
                <span class="stat-label">Most Triggered</span>
                <span class="stat-value">${stats.most_triggered_rule || 'None'}</span>
            </div>
            <div class="stat-item">
                <span class="stat-label">Avg Actions</span>
                <span class="stat-value">${stats.average_actions_per_decision}</span>
            </div>
        `;
    }

    startAutoUpdate() {
        setInterval(() => {
            this.updateEnvironment();
            this.updateSuggestions();
            this.updateStatistics();
            this.syncDeviceStates();
            this.updateAutoModeStatus();
        }, 5000);
        
        this.autoModePolling = setInterval(async () => {
            const statusResult = await this.getAutoModeStatus();
            if (statusResult.success && statusResult.auto_mode) {
                const historyResult = await this.get('/api/ai/decisions/history?limit=1');
                if (historyResult.success && historyResult.data.length > 0) {
                    const lastDecision = historyResult.data[0];
                    const timestamp = new Date(lastDecision.timestamp).getTime();
                    const now = new Date().getTime();
                    
                    if (now - timestamp < 3000 && lastDecision.actions.length > 0) {
                        lastDecision.actions.forEach(action => {
                            this.addAutoModeLog(`${action.rule}: ${action.reason}`);
                        });
                    }
                }
            }
        }, 3000);
    }
    
    async updateAutoModeStatus() {
        const result = await this.getAutoModeStatus();
        if (!result.success) return;
        
        const button = document.getElementById('ai-auto-mode-toggle');
        const statusText = document.getElementById('auto-mode-status');
        const indicator = document.getElementById('auto-mode-indicator');
        
        if (button && statusText) {
            if (result.auto_mode) {
                button.style.background = 'linear-gradient(135deg, #10b981, #059669)';
                button.style.boxShadow = '0 0 20px rgba(16, 185, 129, 0.5)';
                statusText.textContent = 'ON';
                statusText.style.color = '#fff';
                if (indicator) {
                    indicator.style.background = '#10b981';
                    indicator.style.boxShadow = '0 0 15px rgba(16, 185, 129, 0.8)';
                }
            } else {
                button.style.background = 'linear-gradient(135deg, #ef4444, #dc2626)';
                button.style.boxShadow = '0 0 20px rgba(239, 68, 68, 0.3)';
                statusText.textContent = 'OFF';
                statusText.style.color = '#fff';
                if (indicator) {
                    indicator.style.background = '#ef4444';
                    indicator.style.boxShadow = '0 0 15px rgba(239, 68, 68, 0.5)';
                }
            }
        }
    }
    
    addAutoModeLog(message) {
        const logContainer = document.getElementById('auto-mode-log');
        if (!logContainer) return;
        
        const timestamp = new Date().toLocaleTimeString();
        const logEntry = document.createElement('div');
        logEntry.style.marginBottom = '5px';
        logEntry.style.paddingBottom = '5px';
        logEntry.style.borderBottom = '1px solid rgba(255,255,255,0.1)';
        logEntry.innerHTML = `<span style="opacity: 0.5;">[${timestamp}]</span> ${message}`;
        
        logContainer.appendChild(logEntry);
        logContainer.scrollTop = logContainer.scrollHeight;
        
        while (logContainer.children.length > 10) {
            logContainer.removeChild(logContainer.firstChild);
        }
    }
}

// Global instance
const aiClient = new AIClient();

// Initialize AI view when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    // Send command button
    const sendBtn = document.getElementById('ai-send-btn');
    const input = document.getElementById('ai-command-input');
    
    if (sendBtn && input) {
        sendBtn.addEventListener('click', async () => {
            const command = input.value.trim();
            if (!command) return;
            
            aiClient.addMessage(command, true);
            input.value = '';
            
            const result = await aiClient.sendCommand(command);
            
            if (result.success) {
                const response = result.ai_response || result.message;
                const source = result.source === 'ai_model' ? ' (AI)' : '';
                aiClient.addMessage(response + source);
                
                // Force immediate sync after command
                console.log('Command executed, syncing devices...');
                await aiClient.syncDeviceStates();
                
                // Update 3D simulation
                if (typeof apartment3D !== 'undefined' && apartment3D) {
                    apartment3D.updateDeviceStates();
                }
            } else {
                aiClient.addMessage(result.message || 'Sorry, I encountered an error.');
            }
        });
        
        input.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                sendBtn.click();
            }
        });
    }
    
    // Auto execute button
    const autoExecuteBtn = document.getElementById('ai-auto-execute');
    if (autoExecuteBtn) {
        autoExecuteBtn.addEventListener('click', async () => {
            const result = await aiClient.executeAIDecisions();
            
            if (result.success && result.executed > 0) {
                let message = `Executed ${result.executed} AI decisions:\n`;
                result.results.forEach(r => {
                    const deviceName = r.device_id || r.device || r.rule || 'Unknown Device';
                    const reason = r.reason || r.message || 'ML prediction';
                    message += `- ${deviceName} turned ${r.action || 'controlled'} (${reason})\n`;
                });
                aiClient.addMessage(message);
                setTimeout(() => aiClient.syncDeviceStates(), 500);
            } else if (result.success && result.executed === 0) {
                aiClient.addMessage('No actions needed at the moment.');
            } else {
                if (result.error && result.error.includes('fetch')) {
                    const errorMsg = '❌ AI Backend not running! Please start the system using START.bat';
                    aiClient.addMessage(errorMsg);
                } else {
                    aiClient.addMessage('Failed to execute AI decisions. Check console for details.');
                }
            }
        });
    }
    
    // Analyze button
    const analyzeBtn = document.getElementById('ai-analyze');
    if (analyzeBtn) {
        analyzeBtn.addEventListener('click', async () => {
            const result = await aiClient.analyzeEnvironment();
            
            if (result.success) {
                const env = result.environment;
                const actions = result.actions;
                
                let message = `Environment Analysis:\n`;
                message += `- Temperature: ${env.temperature}°C\n`;
                message += `- Motion: ${env.motion ? 'Detected' : 'None'}\n`;
                message += `- Light: ${env.light_level} lux\n\n`;
                
                if (actions.length > 0) {
                    message += `Recommended Actions:\n`;
                    actions.forEach(a => {
                        const deviceName = a.device_id || a.device || a.rule || 'Unknown Device';
                        const reason = a.reason || a.message || 'ML prediction';
                        message += `- ${deviceName}: ${reason}\n`;
                    });
                } else {
                    message += 'No actions recommended.';
                }
                
                aiClient.addMessage(message);
            }
        });
    }
    
    // Auto Mode Toggle Button
    const autoModeBtn = document.getElementById('ai-auto-mode-toggle');
    if (autoModeBtn) {
        autoModeBtn.addEventListener('click', async () => {
            console.log('Auto Mode button clicked!');
            
            const result = await aiClient.toggleAutoMode();
            console.log('Toggle result:', result);
            
            if (result.success) {
                const status = result.data.auto_mode ? 'ENABLED' : 'DISABLED';
                const message = result.data.auto_mode 
                    ? 'Auto Mode ENABLED! Emma is now controlling your home automatically.' 
                    : 'Auto Mode DISABLED. Switched to manual control.';
                
                aiClient.addMessage(message);
                aiClient.addAutoModeLog(message);
                
                // Update button immediately
                await aiClient.updateAutoModeStatus();
            } else {
                console.error('Failed to toggle auto mode:', result);
                
                if (result.error && result.error.includes('fetch')) {
                    const errorMsg = '❌ AI Backend not running! Please start the system using START.bat to enable AI features.';
                    aiClient.addMessage(errorMsg);
                    alert('⚠️ AI Backend Not Running!\n\nPlease close all windows and run START.bat to start all servers.\n\nThe AI backend (port 8090) is required for Auto Mode and AI features.');
                } else {
                    aiClient.addMessage('Failed to toggle auto mode. Check console for details.');
                }
            }
        });
    }
    
    // Start auto updates
    aiClient.startAutoUpdate();
    
    // Initial sync
    setTimeout(() => {
        aiClient.syncDeviceStates();
        aiClient.updateAutoModeStatus();
    }, 1000);
});