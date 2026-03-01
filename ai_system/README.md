# Smart Home AI System

Complete AI system with virtual devices, decision engine, and natural language control.

## Features

✅ **Virtual Devices** - Simulates all smart home devices
✅ **Virtual Sensors** - Generates realistic sensor data
✅ **AI Decision Engine** - Rule-based automation
✅ **Natural Language** - Control devices with voice commands
✅ **Auto Execution** - AI makes decisions automatically
✅ **Dashboard** - Real-time monitoring and control

## Architecture

```
┌─────────────────────────────────────────┐
│         Virtual Smart Home              │
│  - 30+ Virtual Devices                  │
│  - Temperature, Humidity, Motion        │
│  - Smoke, Light Sensors                 │
└──────────────┬──────────────────────────┘
               │
┌──────────────▼──────────────────────────┐
│          AI Decision Engine             │
│  - Rule-based Logic                     │
│  - Environment Analysis                 │
│  - Natural Language Processing          │
│  - Auto Automation                      │
└──────────────┬──────────────────────────┘
               │
┌──────────────▼──────────────────────────┐
│           FastAPI Server                │
│  - REST API                             │
│  - Device Control                       │
│  - AI Commands                          │
└─────────────────────────────────────────┘
```

## Installation

```bash
cd ai_system
pip install -r requirements.txt
```

## Running

```bash
python run_ai.py
```

Server will start on: http://localhost:8090

## API Endpoints

### Devices
- `GET /api/devices` - Get all devices
- `GET /api/devices/{device_id}` - Get device
- `POST /api/devices/control` - Control device
- `POST /api/devices/{device_id}/toggle` - Toggle device

### Sensors
- `GET /api/sensors/read` - Read all sensors
- `GET /api/environment` - Get environment data

### AI
- `POST /api/ai/command` - Send natural language command
- `GET /api/ai/analyze` - Analyze environment
- `POST /api/ai/execute` - Execute AI decisions
- `GET /api/ai/suggestions` - Get AI suggestions
- `GET /api/ai/statistics` - Get AI stats

## Usage Examples

### 1. Natural Language Commands

```bash
curl -X POST http://localhost:8090/api/ai/command \
  -H "Content-Type: application/json" \
  -d '{"command": "Turn on reception light"}'
```

Response:
```json
{
  "success": true,
  "device_id": "rec_light",
  "state": 1,
  "message": "Light System turned ON",
  "ai_response": "Done! I've turned on the Light System."
}
```

### 2. Get Environment Data

```bash
curl http://localhost:8090/api/environment
```

Response:
```json
{
  "success": true,
  "data": {
    "temperature": 25.3,
    "humidity": 45.2,
    "motion": 1,
    "light_level": 320,
    "timestamp": "2026-02-14T20:00:00"
  }
}
```

### 3. Execute AI Decisions

```bash
curl -X POST http://localhost:8090/api/ai/execute
```

Response:
```json
{
  "success": true,
  "executed": 2,
  "results": [
    {
      "device_id": "rec_ac",
      "state": 1,
      "message": "Air Condition turned ON",
      "rule": "High Temperature AC",
      "reason": "Temperature is 28.5°C (high)"
    }
  ]
}
```

### 4. Get AI Suggestions

```bash
curl http://localhost:8090/api/ai/suggestions
```

Response:
```json
{
  "success": true,
  "suggestions": [
    "🌡️ Temperature is 28.5°C. Consider turning on AC.",
    "💡 No motion detected. Turn off lights to save energy."
  ]
}
```

## AI Rules

The AI engine includes these automation rules:

1. **High Temperature AC** - Turn on AC when temp > 28°C and motion detected
2. **Low Temperature AC Off** - Turn off AC when temp < 24°C
3. **No Motion Lights Off** - Turn off lights when no motion
4. **Motion Detected Lights On** - Turn on lights when motion detected
5. **Night Mode** - Dim lights after 22:00
6. **Morning Routine** - Turn on bathroom and kitchen lights at 7:00
7. **Fire Emergency** - Open all windows when smoke detected
8. **Dark Room Lights On** - Turn on lights when light level < 100 lux

## Virtual Devices

### Devices by Room

**Bathroom:**
- Light System
- Water Heater
- Fan System
- Fire Alert (sensor)

**Corridors:**
- Main Light
- Spots Light
- Fire Alert (sensor)

**Reception:**
- Light System
- Smart Window
- Sound System
- Air Condition
- Fire Alert (sensor)

**Outdoor:**
- Camera System
- Light System
- Smart Door

**Room 1:**
- Air Condition
- TV
- Light System
- Smart Window
- Sound System
- Fire Alert (sensor)

**Kitchen:**
- Light System
- Smart Window
- Fan System
- Fire Alert (sensor)

**Room 2:**
- Air Condition
- Sound System
- Light System
- Fire Alert (sensor)

### Environmental Sensors

- Temperature (18-35°C)
- Humidity (30-70%)
- Motion (0/1)
- Smoke (0/1)
- Light Level (0-1000 lux)

## Natural Language Commands

The AI understands these command patterns:

### Turn On/Off
- "Turn on reception light"
- "Turn off kitchen fan"
- "Switch on bedroom AC"
- "Switch off bathroom heater"

### Open/Close
- "Open kitchen window"
- "Close bedroom window"
- "Open outdoor door"

### Room Specific
- "Turn on light in reception"
- "Turn off AC in room 1"
- "Open window in kitchen"

## Integration with Real Hardware

When you're ready to connect real hardware:

### Step 1: Keep AI Engine
The AI decision engine works the same with real or virtual devices.

### Step 2: Replace Virtual Devices

Instead of:
```python
from virtual_devices import virtual_home
```

Use:
```python
from hardware_devices import real_home
```

### Step 3: Update Device Control

Change from:
```python
virtual_home.control_device(device_id, action)
```

To:
```python
mqtt_client.publish(f"smarthome/{device_id}/command", {"status": status})
```

### Step 4: Update Sensor Reading

Change from:
```python
sensor.read_value()  # Fake data
```

To:
```python
mqtt_client.subscribe(f"smarthome/{sensor_id}/sensor")  # Real data
```

## Frontend Integration

The frontend automatically connects to AI system:

1. Open http://localhost:8000
2. Click "AI Control" tab
3. Type commands in chat
4. View environment data
5. See AI suggestions
6. Execute AI decisions

## Testing

### Test Virtual Devices
```python
from virtual_devices import virtual_home

# Get all devices
devices = virtual_home.get_all_devices()
print(f"Total devices: {len(devices)}")

# Control device
result = virtual_home.control_device('rec_light', 'on')
print(result)

# Read sensors
env = virtual_home.get_environment_data()
print(f"Temperature: {env['temperature']}°C")
```

### Test AI Engine
```python
from ai_engine import ai_engine
from virtual_devices import virtual_home

# Get environment
env = virtual_home.get_environment_data()

# Make decision
actions = ai_engine.make_decision(env)
print(f"AI suggests {len(actions)} actions")

# Execute
results = ai_engine.execute_actions(actions, virtual_home)
print(results)
```

### Test Natural Language
```python
from ai_engine import ai_engine
from virtual_devices import virtual_home

# Send command
result = ai_engine.process_command("Turn on reception light", virtual_home)
print(result['ai_response'])
```

## Next Steps

1. ✅ Test virtual devices
2. ✅ Try AI commands
3. ✅ Monitor environment
4. ✅ View AI suggestions
5. ✅ Execute auto decisions
6. 🔄 Connect real hardware (when ready)

## Troubleshooting

### AI not responding
- Check if server is running on port 8090
- Verify API endpoint: http://localhost:8090/api/health

### Commands not working
- Check command format
- Try simpler commands like "turn on light"
- View logs in terminal

### Sensors not updating
- Sensors generate random data every time they're read
- Check /api/environment endpoint

## License

MIT License
