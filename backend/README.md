# Smart Home Backend

FastAPI backend with MQTT support for hardware integration and WebSocket for real-time updates.

## Features

- ✅ RESTful API for device control
- ✅ MQTT broker integration for hardware (ESP32, Arduino, Raspberry Pi)
- ✅ WebSocket for real-time frontend updates
- ✅ SQLite database with async support
- ✅ Ready for AI model integration
- ✅ Energy tracking and analytics
- ✅ Automation rules engine

## Installation

### 1. Install Python Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Install MQTT Broker

**Windows:**
- Download Mosquitto from: https://mosquitto.org/download/
- Install and run as service

**Linux:**
```bash
sudo apt-get install mosquitto mosquitto-clients
sudo systemctl start mosquitto
sudo systemctl enable mosquitto
```

**Mac:**
```bash
brew install mosquitto
brew services start mosquitto
```

### 3. Initialize Database

```bash
cd ../database
python init_db.py
```

## Running the Backend

```bash
cd backend
python run.py
```

The server will start on:
- **API**: http://localhost:8080
- **WebSocket**: ws://localhost:8080/ws
- **Docs**: http://localhost:8080/docs (Swagger UI)

## API Endpoints

### Devices
- `GET /api/devices` - Get all devices
- `GET /api/devices/{device_id}` - Get device by ID
- `GET /api/rooms/{room}/devices` - Get room devices
- `POST /api/devices/{device_id}/toggle` - Toggle device
- `POST /api/devices/{device_id}/set` - Set device status

### Sensors
- `POST /api/sensors/log` - Log sensor data (from hardware)
- `GET /api/sensors/{type}/latest` - Get latest reading
- `GET /api/sensors/{type}/history` - Get sensor history

### Automation
- `GET /api/automation/rules` - Get automation rules
- `POST /api/automation/rules` - Create automation rule

### Energy
- `GET /api/energy/report` - Get energy report
- `POST /api/energy/log` - Log energy usage

### AI
- `GET /api/ai/state` - Get current state for AI
- `GET /api/ai/training-data` - Get training data
- `GET /api/ai/device-pattern/{device_id}` - Get usage pattern

### Hardware
- `POST /api/hardware/register` - Register hardware device
- `GET /api/hardware/status` - Get hardware status

### Health
- `GET /api/health` - Health check

## MQTT Topics

### Commands (Backend → Hardware)
```
smarthome/{device_id}/command     # Control device
smarthome/{device_id}/request     # Request sensor reading
```

### Status (Hardware → Backend)
```
smarthome/{device_id}/status      # Device status update
smarthome/{device_id}/sensor      # Sensor data
smarthome/hardware/{id}/register  # Hardware registration
```

## Hardware Integration

### ESP32/Arduino Example

```cpp
#include <WiFi.h>
#include <PubSubClient.h>

const char* mqtt_server = "192.168.1.100";  // Your backend IP
WiFiClient espClient;
PubSubClient client(espClient);

void setup() {
  Serial.begin(115200);
  pinMode(LED_PIN, OUTPUT);
  
  // Connect to WiFi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
  }
  
  // Connect to MQTT
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);
  
  // Subscribe to commands
  client.subscribe("smarthome/light1/command");
  
  // Register hardware
  client.publish("smarthome/hardware/esp32_001/register", 
    "{\"hardware_id\":\"esp32_001\",\"device_type\":\"light\"}");
}

void callback(char* topic, byte* payload, unsigned int length) {
  String message = "";
  for (int i = 0; i < length; i++) {
    message += (char)payload[i];
  }
  
  // Parse JSON
  if (String(topic) == "smarthome/light1/command") {
    int status = message.toInt();
    digitalWrite(LED_PIN, status);
    
    // Send status back
    client.publish("smarthome/light1/status", 
      String("{\"status\":" + String(status) + "}").c_str());
  }
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();
  
  // Send sensor data every 10 seconds
  static unsigned long lastSend = 0;
  if (millis() - lastSend > 10000) {
    float temp = readTemperature();
    String payload = "{\"type\":\"temperature\",\"value\":" + String(temp) + "}";
    client.publish("smarthome/temp_sensor1/sensor", payload.c_str());
    lastSend = millis();
  }
}
```

### Raspberry Pi Example

```python
import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import json

LED_PIN = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)

def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT")
    client.subscribe("smarthome/light1/command")
    
    # Register hardware
    client.publish("smarthome/hardware/rpi_001/register",
        json.dumps({"hardware_id": "rpi_001", "device_type": "light"}))

def on_message(client, userdata, msg):
    payload = json.loads(msg.payload)
    
    if msg.topic == "smarthome/light1/command":
        status = payload['status']
        GPIO.output(LED_PIN, status)
        
        # Send status back
        client.publish("smarthome/light1/status",
            json.dumps({"status": status}))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("localhost", 1883, 60)
client.loop_forever()
```

## WebSocket Integration

### Frontend Example

```javascript
const ws = new WebSocket('ws://localhost:8080/ws');

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  
  if (data.type === 'device_update') {
    console.log(`Device ${data.device_id} is now ${data.status ? 'ON' : 'OFF'}`);
    updateUI(data.device_id, data.status);
  }
  
  if (data.type === 'sensor_update') {
    console.log(`Sensor ${data.sensor_type}: ${data.value}`);
    updateSensorDisplay(data);
  }
  
  if (data.type === 'alert') {
    showAlert(data.message, data.severity);
  }
};
```

## Testing

### Test API
```bash
# Get all devices
curl http://localhost:8080/api/devices

# Toggle device
curl -X POST http://localhost:8080/api/devices/rec_light/toggle

# Log sensor data
curl -X POST "http://localhost:8080/api/sensors/log?sensor_type=temperature&value=25.5&room=reception"

# Health check
curl http://localhost:8080/api/health
```

### Test MQTT
```bash
# Subscribe to all topics
mosquitto_sub -h localhost -t "smarthome/#" -v

# Publish command
mosquitto_pub -h localhost -t "smarthome/light1/command" -m '{"status":1}'

# Publish sensor data
mosquitto_pub -h localhost -t "smarthome/temp1/sensor" -m '{"type":"temperature","value":25.5}'
```

## Architecture

```
┌─────────────┐     WebSocket      ┌─────────────┐
│  Frontend   │◄──────────────────►│   Backend   │
│  (Browser)  │     HTTP API       │  (FastAPI)  │
└─────────────┘                    └──────┬──────┘
                                          │
                                          │ MQTT
                                          │
                                    ┌─────▼──────┐
                                    │   MQTT     │
                                    │   Broker   │
                                    └─────┬──────┘
                                          │
                    ┌─────────────────────┼─────────────────────┐
                    │                     │                     │
              ┌─────▼─────┐         ┌────▼────┐          ┌────▼────┐
              │   ESP32   │         │ Arduino │          │   RPi   │
              │  Devices  │         │ Devices │          │ Devices │
              └───────────┘         └─────────┘          └─────────┘
```

## Troubleshooting

### MQTT Connection Failed
- Make sure Mosquitto is running: `mosquitto -v`
- Check firewall settings
- Verify broker address in `mqtt_manager.py`

### Database Not Found
- Run `python init_db.py` in database folder
- Check database path in `database_manager.py`

### WebSocket Not Connecting
- Check if backend is running
- Verify WebSocket URL in frontend
- Check browser console for errors

## Production Deployment

### Using Docker

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "run.py"]
```

### Using systemd (Linux)

```ini
[Unit]
Description=Smart Home Backend
After=network.target

[Service]
Type=simple
User=smarthome
WorkingDirectory=/home/smarthome/backend
ExecStart=/usr/bin/python3 run.py
Restart=always

[Install]
WantedBy=multi-user.target
```

## License

MIT License
