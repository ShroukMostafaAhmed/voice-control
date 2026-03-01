@echo off
cls
color 0A
echo ========================================
echo   Smart Home System - Full Startup
echo ========================================
echo.
echo Starting all components:
echo   [1] Database Initialization
echo   [2] Backend Server (Port 8080)
echo   [3] AI System + Chatbot (Port 8090)
echo   [4] Frontend Server (Port 8000)
echo.
echo New Features:
echo   - Voice Control (Toggle ON/OFF)
echo   - Dynamic Commands (All lights, Everything, etc.)
echo   - Bigger 3D Simulation (70%% larger)
echo   - TinyLlama AI Model (637 MB)
echo.
echo ========================================
echo.

echo [1/4] Initializing Database...
cd database
python init_db.py
if errorlevel 1 (
    echo ERROR: Database initialization failed!
    pause
    exit /b 1
)
cd ..
echo ✓ Database initialized!
timeout /t 2 /nobreak > nul

echo.
echo [2/4] Starting Backend Server (Port 8080)...
start "Backend Server" cmd /k "cd backend && python run.py"
timeout /t 3 /nobreak > nul
echo ✓ Backend Server started!

echo.
echo [3/4] Starting AI System + Chatbot (Port 8090)...
start "AI System + Chatbot" cmd /k "cd ai_system && python run_ai.py"
timeout /t 3 /nobreak > nul
echo ✓ AI System + Chatbot started!

echo.
echo [4/4] Starting Frontend Server (Port 8000)...
start "Frontend Server" cmd /k "cd frontend && python -m http.server 8000"
timeout /t 3 /nobreak > nul
echo ✓ Frontend Server started!

echo.
echo ========================================
echo   All Systems Started Successfully!
echo ========================================
echo.
echo 🌐 Frontend:  http://localhost:8000
echo 🔧 Backend:   http://localhost:8080
echo 🤖 AI System: http://localhost:8090
echo 📚 API Docs:  http://localhost:8090/docs
echo.
echo ========================================
echo   Main Features:
echo ========================================
echo.
echo ✓ Control Panel - 33 devices across 7 rooms
echo ✓ 3D Simulation - 70%% BIGGER visual view
echo ✓ AI Chatbot - Natural language commands
echo ✓ Voice Control - Toggle ON/OFF (NEW!)
echo ✓ Dynamic Commands - Multiple devices (NEW!)
echo ✓ Auto Mode - AI automation rules
echo ✓ TinyLlama Model - 637 MB lightweight AI
echo.
echo ========================================
echo   Voice Control (NEW!):
echo ========================================
echo.
echo 🎤 AUTO-START: Microphone starts automatically!
echo 💤 WAKE WORD: Say "Hey My Home" to activate
echo 😴 SLEEP WORD: Say "Sleep" to deactivate
echo 🔄 ALWAYS ON: Mic listens continuously
echo 💬 VOICE FEEDBACK: AI responds with voice
echo.
echo Wake Words:
echo   - "Hey My Home"
echo   - "Hi My Home"
echo.
echo Sleep Words:
echo   - "Sleep"
echo   - "Sleep My Home"
echo   - "Go to Sleep"
echo.
echo ========================================
echo   Dynamic Commands (NEW!):
echo ========================================
echo.
echo ✓ "Turn on all lights"
echo ✓ "Turn off everything"
echo ✓ "Turn on all devices in reception"
echo ✓ "Turn off all lights in room 1"
echo ✓ "Turn on all AC"
echo ✓ "Turn off all fans in kitchen"
echo.
echo Opening browser in 3 seconds...
timeout /t 3 /nobreak > nul
start http://localhost:8000

echo.
echo ========================================
echo   System Running Successfully!
echo ========================================
echo.
echo You should see 3 windows:
echo   - Backend Server (Port 8080)
echo   - AI System + Chatbot (Port 8090)
echo   - Frontend Server (Port 8000)
echo.
echo ========================================
echo   Quick Start Guide:
echo ========================================
echo.
echo 1. Control Panel Tab:
echo    - Click device toggles to control manually
echo    - Changes persist and sync with AI
echo.
echo 2. 3D Simulation Tab:
echo    - View apartment in 3D (70%% bigger!)
echo    - Microphone AUTO-STARTS in 2 seconds
echo    - Say "Hey My Home" to wake system
echo    - Say "Sleep" to put system to sleep
echo    - Speak commands continuously
echo.
echo 3. AI Control Tab:
echo    - Type commands in chat
echo    - Enable Auto Mode for automation
echo    - Toggle TinyLlama model ON/OFF
echo.
echo ========================================
echo   Voice Command Examples:
echo ========================================
echo.
echo FIRST: Say "Hey My Home" to wake up!
echo.
echo Single Device:
echo   - "Turn on reception light"
echo   - "Turn off room 1 TV"
echo   - "Open kitchen window"
echo.
echo Multiple Devices:
echo   - "Turn on all lights"
echo   - "Turn off everything"
echo   - "Turn on all devices in reception"
echo   - "Turn off all lights in room 1"
echo   - "Turn on all AC"
echo.
echo To Sleep:
echo   - "Sleep"
echo   - "Sleep My Home"
echo   - "Go to Sleep"
echo.
echo Rooms Supported:
echo   - Reception, Kitchen, Bathroom
echo   - Room 1 / Room One / Bedroom 1 / R1
echo   - Room 2 / Room Two / Bedroom 2 / R2
echo   - Corridors, Out Door
echo.
echo Press any key to STOP all servers...
pause > nul

echo.
echo ========================================
echo   Stopping all servers...
echo ========================================
echo.
taskkill /FI "WINDOWTITLE eq Backend Server*" /T /F 2>nul
taskkill /FI "WINDOWTITLE eq AI System*" /T /F 2>nul
taskkill /FI "WINDOWTITLE eq Frontend Server*" /T /F 2>nul
echo.
echo ✓ All servers stopped.
echo.
timeout /t 2 /nobreak > nul
