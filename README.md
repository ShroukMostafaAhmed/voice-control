# Smart Home Control System

Complete smart home control system with AI, 3D Simulation, and full control interface.

## Quick Start

### One command to run everything:
```bash
START.bat
```

This will start:
- Database (SQLite)
- Backend Server (port 8080)
- AI System (port 8090)
- Frontend (port 8000)
- Browser automatically

## Links

- **Frontend:** http://localhost:8000
- **Backend API:** http://localhost:8080
- **Backend Docs:** http://localhost:8080/docs
- **AI System:** http://localhost:8090
- **AI Docs:** http://localhost:8090/docs

## Features

### 1. Control Panel
- Manual control for all devices
- 7 rooms, 30+ devices
- Real-time updates

### 2. 3D Simulation
- 3D apartment visualization
- Real-time device animations
- OrbitControls for camera

### 3. AI Control
- **Auto Mode:** AI controls automatically (8 smart rules)
- **Chatbot:** Natural language commands (with optional Mistral)
- **Environment Monitor:** Temperature, humidity, motion, light
- **AI Suggestions:** Smart recommendations

### 4. Voice Control (NEW!)
- Toggle ON/OFF microphone button
- Continuous listening mode
- Dynamic commands support
- Text-to-Speech responses

## Auto Mode

### How it works:
1. Click "Auto Mode" button → turns green
2. AI checks environment every 10 seconds
3. Applies smart rules automatically
4. Changes appear in Control Panel & 3D Simulation

### Smart Rules (8 rules):
1. **High Temperature** - temp >28°C + motion → turn on AC
2. **Low Temperature** - temp <24°C → turn off AC
3. **No Motion** - no motion → turn off corridor lights
4. **Motion Detected** - motion → turn on corridor lights
5. **Night Mode** - after 10 PM → dim lights
6. **Morning Routine** - 7 AM → turn on bathroom & kitchen lights
7. **Fire Emergency** - smoke → open all windows
8. **Dark Room** - light <100 lux + motion → turn on lights

## Voice Control

### Features:
- **Location:** Top-right button in 3D Simulation tab
- **Toggle:** Click once = ON (green), Click again = OFF (gray)
- **Continuous:** No repeated clicks needed
- **Dynamic Commands:** Control multiple devices at once

### Example Commands:

**Single Device:**
- "Turn on reception light"
- "Turn off room 1 TV"
- "Open kitchen window"

**Multiple Devices:**
- "Turn on all lights"
- "Turn off everything"
- "Turn on all devices in reception"
- "Turn off all lights in room 1"
- "Turn on all AC"

## Chatbot (Optional)

### Without Mistral (default):
- Simple commands: "Turn on reception light"
- Very fast (< 100ms)

### With Mistral (advanced):
```bash
# Install Ollama
# From: https://ollama.ai/download

# Install Mistral or TinyLlama
ollama pull tinyllama
```

- Complex commands: "I'm hot" → turns on AC
- Natural language understanding

## Project Structure

```
├── START.bat              # Main startup file
├── README.md              # This file
├── SETUP.md               # Detailed setup guide
│
├── frontend/              # User interface
│   ├── index.html
│   ├── style.css
│   ├── app.js            # Control Panel
│   ├── apartment3d.js    # 3D Simulation
│   ├── ai_client.js      # AI Integration
│   ├── voice_control.js  # Voice Control
│   └── data.js           # Device data
│
├── ai_system/            # AI System
│   ├── run_ai.py         # Entry point
│   ├── ai_api.py         # FastAPI Server
│   ├── ai_engine.py      # Decision Engine
│   ├── virtual_devices.py # Device simulation
│   └── mistral_client.py # Mistral integration
│
├── backend/              # Backend (optional)
│   ├── main.py
│   ├── database_manager.py
│   └── mqtt_manager.py
│
└── database/             # Database (optional)
    ├── schema.sql
    └── init_db.py
```

## Troubleshooting

### Problem: AI System not working
```bash
# Check requirements
cd ai_system
pip install -r requirements.txt

# Run manually
python run_ai.py
```

### Problem: Devices not responding
- Refresh page (F5)
- Make sure AI System is running (port 8090)
- Open Console (F12) and check errors

### Problem: Auto Mode not working
- Make sure button is green (ON)
- Check Terminal for errors
- Wait 10 seconds for first check

### Problem: Voice Control not working
- Allow microphone access in browser
- Use Chrome or Edge (best support)
- Check microphone settings in system

## Requirements

### Install requirements (once only):
```bash
# AI System
cd ai_system
pip install -r requirements.txt

# Backend
cd backend
pip install -r requirements.txt
```

After installation, run:
```bash
START.bat
```

## Notes

### Auto Mode vs Manual Control:

**Auto Mode (ON):**
- AI controls automatically
- Checks every 10 seconds
- Applies smart rules

**Manual Control (OFF):**
- Full manual control
- Devices stay in their state
- No automatic changes

### To connect real hardware:
1. Replace `virtual_devices.py` with `hardware_devices.py`
2. Use MQTT to communicate with ESP32/Arduino
3. AI Engine stays the same!

## Enjoy!

System is ready to use. Run `START.bat` and start controlling your smart home!

---

**For more details:** See `SETUP.md`
