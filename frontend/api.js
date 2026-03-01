// API Client for Backend Communication

class SmartHomeAPI {
    constructor(baseURL = 'http://localhost:8080') {
        this.baseURL = baseURL;
        this.ws = null;
        this.wsCallbacks = [];
    }

    // ==================== HTTP API ====================

    async get(endpoint) {
        try {
            const response = await fetch(`${this.baseURL}${endpoint}`);
            const data = await response.json();
            return data;
        } catch (error) {
            console.error(`API GET error: ${endpoint}`, error);
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
            const data = await response.json();
            return data;
        } catch (error) {
            console.error(`API POST error: ${endpoint}`, error);
            return { success: false, error: error.message };
        }
    }

    // ==================== DEVICE API ====================

    async getAllDevices() {
        return await this.get('/api/devices');
    }

    async getDevice(deviceId) {
        return await this.get(`/api/devices/${deviceId}`);
    }

    async getRoomDevices(room) {
        return await this.get(`/api/rooms/${room}/devices`);
    }

    async toggleDevice(deviceId, triggeredBy = 'user') {
        return await this.post(`/api/devices/${deviceId}/toggle?triggered_by=${triggeredBy}`);
    }

    async setDeviceStatus(deviceId, status, triggeredBy = 'user') {
        return await this.post(`/api/devices/${deviceId}/set?status=${status}&triggered_by=${triggeredBy}`);
    }

    // ==================== SENSOR API ====================

    async logSensorData(sensorType, value, room) {
        return await this.post(`/api/sensors/log?sensor_type=${sensorType}&value=${value}&room=${room}`);
    }

    async getLatestSensor(sensorType, room = null) {
        const roomParam = room ? `?room=${room}` : '';
        return await this.get(`/api/sensors/${sensorType}/latest${roomParam}`);
    }

    async getSensorHistory(sensorType, hours = 24) {
        return await this.get(`/api/sensors/${sensorType}/history?hours=${hours}`);
    }

    // ==================== AUTOMATION API ====================

    async getAutomationRules() {
        return await this.get('/api/automation/rules');
    }

    async createAutomationRule(ruleName, condition, action, priority = 1) {
        return await this.post(`/api/automation/rules?rule_name=${ruleName}&condition=${condition}&action=${action}&priority=${priority}`);
    }

    // ==================== ENERGY API ====================

    async getEnergyReport(days = 7) {
        return await this.get(`/api/energy/report?days=${days}`);
    }

    async logEnergyUsage(deviceId, powerWatts, durationMinutes) {
        return await this.post(`/api/energy/log?device_id=${deviceId}&power_watts=${powerWatts}&duration_minutes=${durationMinutes}`);
    }

    // ==================== ALERTS API ====================

    async getAlerts() {
        return await this.get('/api/alerts');
    }

    async createAlert(alertType, severity, message, room = null) {
        const roomParam = room ? `&room=${room}` : '';
        return await this.post(`/api/alerts?alert_type=${alertType}&severity=${severity}&message=${message}${roomParam}`);
    }

    // ==================== AI API ====================

    async getAIState() {
        return await this.get('/api/ai/state');
    }

    async getTrainingData(days = 30) {
        return await this.get(`/api/ai/training-data?days=${days}`);
    }

    async getDevicePattern(deviceId) {
        return await this.get(`/api/ai/device-pattern/${deviceId}`);
    }

    // ==================== STATISTICS API ====================

    async getDeviceStats() {
        return await this.get('/api/stats/devices');
    }

    async getSystemStats() {
        return await this.get('/api/stats/system');
    }

    // ==================== HARDWARE API ====================

    async registerHardware(deviceId, hardwareId, deviceType) {
        return await this.post(`/api/hardware/register?device_id=${deviceId}&hardware_id=${hardwareId}&device_type=${deviceType}`);
    }

    async getHardwareStatus() {
        return await this.get('/api/hardware/status');
    }

    // ==================== HEALTH CHECK ====================

    async healthCheck() {
        return await this.get('/api/health');
    }

    // ==================== WEBSOCKET ====================

    connectWebSocket() {
        const wsURL = this.baseURL.replace('http', 'ws') + '/ws';
        
        this.ws = new WebSocket(wsURL);

        this.ws.onopen = () => {
            console.log('✓ WebSocket connected');
        };

        this.ws.onmessage = (event) => {
            try {
                const data = JSON.parse(event.data);
                console.log('📨 WebSocket message:', data);
                
                // Call all registered callbacks
                this.wsCallbacks.forEach(callback => callback(data));
            } catch (error) {
                console.error('WebSocket message error:', error);
            }
        };

        this.ws.onerror = (error) => {
            console.error('✗ WebSocket error:', error);
        };

        this.ws.onclose = () => {
            console.log('✗ WebSocket disconnected');
            // Reconnect after 3 seconds
            setTimeout(() => this.connectWebSocket(), 3000);
        };

        // Send ping every 30 seconds to keep connection alive
        setInterval(() => {
            if (this.ws && this.ws.readyState === WebSocket.OPEN) {
                this.ws.send(JSON.stringify({ type: 'ping' }));
            }
        }, 30000);
    }

    onWebSocketMessage(callback) {
        this.wsCallbacks.push(callback);
    }

    disconnectWebSocket() {
        if (this.ws) {
            this.ws.close();
        }
    }
}

// Create global API instance
const api = new SmartHomeAPI();
