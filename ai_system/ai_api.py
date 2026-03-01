"""
AI System API
FastAPI server for AI control
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional
import uvicorn
import asyncio

from virtual_devices import virtual_home
from ai_engine_advanced import advanced_ai_engine as ai_engine
from mistral_client import mistral_client

app = FastAPI(title="Smart Home AI System", version="1.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request models
class CommandRequest(BaseModel):
    command: str
    use_mistral: Optional[bool] = True  # Use Mistral by default

class DeviceControlRequest(BaseModel):
    device_id: str
    action: str  # on, off, toggle

class AutoModeRequest(BaseModel):
    enabled: bool

# Auto mode background task
auto_mode_task = None

async def auto_control_loop():
    """Background task for auto control"""
    print("[AUTO MODE] Background task started")
    
    while True:
        try:
            if ai_engine.get_auto_mode_status():
                # Get environment data
                env_data = virtual_home.get_environment_data()
                
                print(f"\n[AUTO MODE] Checking environment...")
                print(f"  Temperature: {env_data['temperature']}°C")
                print(f"  Motion: {'Detected' if env_data['motion'] else 'None'}")
                print(f"  Light Level: {env_data['light_level']} lux")
                
                # Make AI decisions
                actions = ai_engine.make_decision(env_data)
                
                # Execute actions
                if actions:
                    results = ai_engine.execute_actions(actions, virtual_home)
                    print(f"[AUTO MODE] ✓ Executed {len(results)} actions:")
                    for result in results:
                        print(f"  → {result.get('message', 'Unknown action')} ({result.get('reason', 'No reason')})")
                else:
                    print(f"[AUTO MODE] No actions needed")
            
            # Wait 10 seconds before next check
            await asyncio.sleep(10)
        except Exception as e:
            print(f"[AUTO MODE ERROR] {e}")
            await asyncio.sleep(10)

@app.on_event("startup")
async def startup_event():
    """Start background tasks"""
    global auto_mode_task
    auto_mode_task = asyncio.create_task(auto_control_loop())
    print("[AUTO MODE] Background task started")

@app.on_event("shutdown")
async def shutdown_event():
    """Stop background tasks"""
    global auto_mode_task
    if auto_mode_task:
        auto_mode_task.cancel()
        print("[AUTO MODE] Background task stopped")

# ==================== DEVICE ENDPOINTS ====================

@app.get("/api/devices")
async def get_all_devices():
    """Get all devices"""
    devices = virtual_home.get_all_devices()
    return {"success": True, "data": devices, "count": len(devices)}

@app.get("/api/devices/{device_id}")
async def get_device(device_id: str):
    """Get specific device"""
    device = virtual_home.get_device(device_id)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    return {"success": True, "data": device.get_state()}

@app.get("/api/rooms/{room}/devices")
async def get_room_devices(room: str):
    """Get devices in a room"""
    devices = virtual_home.get_room_devices(room)
    return {"success": True, "data": devices, "count": len(devices)}

@app.post("/api/devices/control")
async def control_device(request: DeviceControlRequest):
    """Control a device"""
    result = virtual_home.control_device(request.device_id, request.action)
    return result

@app.post("/api/devices/{device_id}/toggle")
async def toggle_device(device_id: str):
    """Toggle device"""
    result = virtual_home.control_device(device_id, 'toggle')
    return result

# ==================== SENSOR ENDPOINTS ====================

@app.get("/api/sensors/read")
async def read_all_sensors():
    """Read all sensors"""
    readings = virtual_home.read_all_sensors()
    return {"success": True, "data": readings}

@app.get("/api/environment")
async def get_environment():
    """Get environment data"""
    env_data = virtual_home.get_environment_data()
    return {"success": True, "data": env_data}

# ==================== AI ENDPOINTS ====================

@app.post("/api/ai/command")
async def process_ai_command(request: CommandRequest):
    """Process natural language command with AI model or fallback"""
    
    # Check if AI model should be used
    if request.use_mistral and mistral_client.is_available():
        # Get environment context
        env_data = virtual_home.get_environment_data()
        
        # Parse command with AI model
        parsed = mistral_client.parse_command(request.command, env_data)
        
        # If AI model succeeded
        if parsed['action'] == 'control_device' and parsed['device_id']:
            # Execute command
            result = virtual_home.control_device(
                parsed['device_id'], 
                parsed['command']
            )
            
            if result['success']:
                # Generate response with AI model (with fallback)
                try:
                    ai_response = mistral_client.generate_response(result, request.command)
                    result['ai_response'] = ai_response
                except:
                    result['ai_response'] = result.get('message', 'Done')
                
                result['source'] = 'ai_model'
                result['confidence'] = parsed['confidence']
            
            return result
    
    # Fallback to simple parsing using rule engine
    result = ai_engine.rule_engine.process_command(request.command, virtual_home)
    result['source'] = 'fallback'
    return result

@app.get("/api/ai/analyze")
async def analyze_environment():
    """Analyze environment and get AI decisions"""
    env_data = virtual_home.get_environment_data()
    actions = ai_engine.make_decision(env_data)
    
    return {
        "success": True,
        "environment": env_data,
        "actions": actions,
        "count": len(actions)
    }

@app.post("/api/ai/execute")
async def execute_ai_decisions():
    """Execute AI decisions automatically"""
    env_data = virtual_home.get_environment_data()
    actions = ai_engine.make_decision(env_data)
    results = ai_engine.execute_actions(actions, virtual_home)
    
    return {
        "success": True,
        "executed": len(results),
        "results": results
    }

@app.get("/api/ai/suggestions")
async def get_ai_suggestions():
    """Get AI suggestions"""
    env_data = virtual_home.get_environment_data()
    suggestions = ai_engine.get_suggestions(env_data)
    
    return {
        "success": True,
        "suggestions": suggestions,
        "environment": env_data
    }

@app.get("/api/ai/statistics")
async def get_ai_statistics():
    """Get AI statistics"""
    stats = ai_engine.get_statistics()
    return {"success": True, "data": stats}

@app.post("/api/ai/auto-mode/toggle")
async def toggle_auto_mode():
    """Toggle auto control mode"""
    result = ai_engine.toggle_auto_mode()
    return {"success": True, "data": result}

@app.get("/api/ai/auto-mode/status")
async def get_auto_mode_status():
    """Get auto mode status"""
    status = ai_engine.get_auto_mode_status()
    return {"success": True, "auto_mode": status}

@app.get("/api/ai/auto-mode/logs")
async def get_auto_mode_logs():
    """Get recent auto mode actions"""
    # Get last 5 decisions
    recent_decisions = ai_engine.decisions_log[-5:]
    logs = []
    
    for decision in recent_decisions:
        if decision['actions']:
            logs.append({
                'timestamp': decision['timestamp'],
                'actions': [
                    {
                        'rule': action['rule'],
                        'reason': action['reason'],
                        'devices': action['devices']
                    }
                    for action in decision['actions']
                ]
            })
    
    return {"success": True, "logs": logs}

@app.get("/api/ai/decisions/history")
async def get_decisions_history(limit: int = 20):
    """Get AI decisions history"""
    history = ai_engine.decisions_log[-limit:]
    return {"success": True, "data": history, "count": len(history)}

# ==================== AUTOMATION ENDPOINTS ====================

@app.get("/api/automation/rules")
async def get_automation_rules():
    """Get all automation rules"""
    rules = []
    for rule in ai_engine.rules:
        rules.append({
            'name': rule['name'],
            'action': rule['action'],
            'priority': rule['priority'],
            'devices': rule['devices']
        })
    return {"success": True, "data": rules}

# ==================== SYSTEM ENDPOINTS ====================

@app.get("/api/system/status")
async def get_system_status():
    """Get system status"""
    devices = virtual_home.get_all_devices()
    active_devices = sum(1 for d in devices if d['state'] == 1)
    
    return {
        "success": True,
        "data": {
            "total_devices": len(devices),
            "active_devices": active_devices,
            "ai_decisions": len(ai_engine.decisions_log),
            "status": "operational"
        }
    }

@app.get("/api/health")
async def health_check():
    """Health check"""
    return {
        "status": "healthy",
        "service": "AI Smart Home System",
        "version": "1.0.0"
    }

# ==================== SIMULATION ENDPOINTS ====================

@app.post("/api/simulation/random-event")
async def trigger_random_event():
    """Trigger random simulation event"""
    import random
    
    events = [
        {"type": "motion", "message": "Motion detected in corridors"},
        {"type": "temperature", "message": "Temperature spike detected"},
        {"type": "door", "message": "Door opened"},
    ]
    
    event = random.choice(events)
    
    # Execute AI analysis
    env_data = virtual_home.get_environment_data()
    actions = ai_engine.make_decision(env_data)
    
    return {
        "success": True,
        "event": event,
        "ai_response": actions
    }

if __name__ == "__main__":
    print("=" * 60)
    print("Smart Home AI System")
    print("=" * 60)
    print("\nStarting AI API Server...")
    print("   - API: http://localhost:8090")
    print("   - Docs: http://localhost:8090/docs")
    print("\nTry these commands:")
    print("   - 'Turn on reception light'")
    print("   - 'Turn off kitchen fan'")
    print("   - 'Open bedroom window'")
    print("\n" + "=" * 60 + "\n")
    
    uvicorn.run(app, host="0.0.0.0", port=8090, log_level="info")


# ==================== ADVANCED AI ENDPOINTS ====================

@app.get("/api/ai/system/info")
async def get_system_info():
    """Get AI system information"""
    info = ai_engine.get_system_info()
    return {"success": True, "data": info}

@app.get("/api/ai/system/stats")
async def get_system_stats():
    """Get detailed AI statistics"""
    stats = ai_engine.get_statistics()
    return {"success": True, "data": stats}

@app.get("/api/ai/models/status")
async def get_models_status():
    """Get ML model status"""
    return {
        "success": True,
        "data": {
            "ml_model_loaded": bool(ai_engine.ml_engine.model),
            "ml_available": bool(ai_engine.ml_engine.model),
            "devices_predicted": len(ai_engine.ml_engine.device_columns) if ai_engine.ml_engine.model else 0,
            "mistral_available": ai_engine.mistral.is_available(),
            "mistral_model": ai_engine.mistral.model_name,
            "rule_engine_ready": True
        }
    }

@app.post("/api/ai/test/scenario")
async def test_scenario(
    temperature: float = 25,
    humidity: float = 50,
    motion: int = 0,
    light_level: float = 300,
    smoke_detected: int = 0
):
    """Test AI with custom scenario"""
    
    env_data = {
        'temperature': temperature,
        'humidity': humidity,
        'motion': motion,
        'light_level': light_level,
        'smoke_detected': smoke_detected
    }
    
    # Make decision
    actions = ai_engine.make_decision(env_data)
    
    # Don't execute, just return predictions
    return {
        "success": True,
        "scenario": env_data,
        "predictions": actions,
        "count": len(actions)
    }

@app.get("/api/ai/health")
async def ai_health_check():
    """Check AI system health"""
    return {
        "success": True,
        "status": "healthy",
        "components": {
            "ml_model": "loaded" if ai_engine.ml_engine.model else "not_loaded",
            "rule_engine": "ready",
            "mistral": "available" if ai_engine.mistral.is_available() else "not_available",
            "virtual_devices": "ready"
        },
        "timestamp": datetime.now().isoformat()
    }

# ==================== CONFIGURATION ENDPOINTS ====================

@app.post("/api/ai/config/use_ml")
async def set_use_ml(enabled: bool):
    """Enable/disable ML models"""
    ai_engine.use_ml = enabled
    return {
        "success": True,
        "message": f"ML models {'enabled' if enabled else 'disabled'}",
        "use_ml": ai_engine.use_ml
    }

@app.post("/api/ai/config/use_mistral")
async def set_use_mistral(enabled: bool):
    """Enable/disable Mistral AI"""
    ai_engine.use_mistral = enabled
    return {
        "success": True,
        "message": f"Mistral AI {'enabled' if enabled else 'disabled'}",
        "use_mistral": ai_engine.use_mistral
    }

@app.get("/api/ai/config")
async def get_config():
    """Get current AI configuration"""
    return {
        "success": True,
        "config": {
            "use_ml": ai_engine.use_ml,
            "use_mistral": ai_engine.use_mistral,
            "emergency_use_rules": ai_engine.emergency_use_rules,
            "auto_mode": ai_engine.auto_mode
        }
    }

# Import datetime for health check
from datetime import datetime
