"""
Smart Home Backend API
FastAPI + MQTT + WebSocket for real-time control
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import List, Dict, Optional
import asyncio
import json
from datetime import datetime

from database_manager import DatabaseManager
from mqtt_manager import MQTTManager
from websocket_manager import WebSocketManager

# Initialize FastAPI
app = FastAPI(title="Smart Home API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize managers
db = DatabaseManager()
mqtt = MQTTManager()
ws_manager = WebSocketManager()

# ==================== STARTUP/SHUTDOWN ====================

@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    await db.initialize()
    await mqtt.connect()
    print("✓ Backend services started")

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    await mqtt.disconnect()
    await db.close()
    print("✓ Backend services stopped")

# ==================== WEBSOCKET ====================

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket for real-time updates"""
    await ws_manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            
            # Handle different message types
            if message.get("type") == "ping":
                await websocket.send_json({"type": "pong"})
            
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket)

# ==================== DEVICE ENDPOINTS ====================

@app.get("/api/devices")
async def get_all_devices():
    """Get all devices"""
    devices = await db.get_all_devices()
    return {"success": True, "data": devices}

@app.get("/api/devices/{device_id}")
async def get_device(device_id: str):
    """Get device by ID"""
    device = await db.get_device_by_id(device_id)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    return {"success": True, "data": device}

@app.get("/api/rooms/{room}/devices")
async def get_room_devices(room: str):
    """Get all devices in a room"""
    devices = await db.get_devices_by_room(room)
    return {"success": True, "data": devices}

@app.post("/api/devices/{device_id}/toggle")
async def toggle_device(device_id: str, triggered_by: str = "user"):
    """Toggle device on/off"""
    device = await db.get_device_by_id(device_id)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    
    new_status = 1 if device['status'] == 0 else 0
    
    # Update database
    await db.update_device_status(device_id, new_status, triggered_by)
    
    # Send MQTT command to hardware
    await mqtt.publish_device_command(device_id, new_status)
    
    # Broadcast to all WebSocket clients
    await ws_manager.broadcast({
        "type": "device_update",
        "device_id": device_id,
        "status": new_status,
        "triggered_by": triggered_by,
        "timestamp": datetime.now().isoformat()
    })
    
    return {
        "success": True,
        "data": {
            "device_id": device_id,
            "status": new_status
        }
    }

@app.post("/api/devices/{device_id}/set")
async def set_device_status(device_id: str, status: int, triggered_by: str = "user"):
    """Set device status directly"""
    if status not in [0, 1]:
        raise HTTPException(status_code=400, detail="Status must be 0 or 1")
    
    await db.update_device_status(device_id, status, triggered_by)
    await mqtt.publish_device_command(device_id, status)
    
    await ws_manager.broadcast({
        "type": "device_update",
        "device_id": device_id,
        "status": status,
        "triggered_by": triggered_by,
        "timestamp": datetime.now().isoformat()
    })
    
    return {"success": True, "data": {"device_id": device_id, "status": status}}

# ==================== SENSOR ENDPOINTS ====================

@app.post("/api/sensors/log")
async def log_sensor_data(sensor_type: str, value: float, room: str):
    """Log sensor reading (from hardware)"""
    await db.log_sensor_data(sensor_type, value, room)
    
    # Broadcast to WebSocket clients
    await ws_manager.broadcast({
        "type": "sensor_update",
        "sensor_type": sensor_type,
        "value": value,
        "room": room,
        "timestamp": datetime.now().isoformat()
    })
    
    return {"success": True}

@app.get("/api/sensors/{sensor_type}/latest")
async def get_latest_sensor(sensor_type: str, room: Optional[str] = None):
    """Get latest sensor reading"""
    data = await db.get_latest_sensor_data(sensor_type, room)
    return {"success": True, "data": data}

@app.get("/api/sensors/{sensor_type}/history")
async def get_sensor_history(sensor_type: str, hours: int = 24):
    """Get sensor history"""
    data = await db.get_sensor_history(sensor_type, hours)
    return {"success": True, "data": data}

# ==================== AUTOMATION ENDPOINTS ====================

@app.get("/api/automation/rules")
async def get_automation_rules():
    """Get all automation rules"""
    rules = await db.get_active_rules()
    return {"success": True, "data": rules}

@app.post("/api/automation/rules")
async def create_automation_rule(rule_name: str, condition: str, action: str, priority: int = 1):
    """Create new automation rule"""
    await db.add_automation_rule(rule_name, condition, action, priority)
    return {"success": True}

# ==================== ENERGY ENDPOINTS ====================

@app.get("/api/energy/report")
async def get_energy_report(days: int = 7):
    """Get energy usage report"""
    report = await db.get_energy_report(days)
    return {"success": True, "data": report}

@app.post("/api/energy/log")
async def log_energy_usage(device_id: str, power_watts: float, duration_minutes: float):
    """Log energy usage"""
    await db.log_energy_usage(device_id, power_watts, duration_minutes)
    return {"success": True}

# ==================== ALERTS ENDPOINTS ====================

@app.get("/api/alerts")
async def get_alerts():
    """Get unresolved alerts"""
    alerts = await db.get_unresolved_alerts()
    return {"success": True, "data": alerts}

@app.post("/api/alerts")
async def create_alert(alert_type: str, severity: str, message: str, room: Optional[str] = None):
    """Create new alert"""
    await db.create_alert(alert_type, severity, message, room)
    
    # Broadcast alert
    await ws_manager.broadcast({
        "type": "alert",
        "alert_type": alert_type,
        "severity": severity,
        "message": message,
        "room": room,
        "timestamp": datetime.now().isoformat()
    })
    
    return {"success": True}

# ==================== AI ENDPOINTS ====================

@app.get("/api/ai/state")
async def get_ai_state():
    """Get current system state for AI"""
    state = await db.get_current_state_for_ai()
    return {"success": True, "data": state}

@app.get("/api/ai/training-data")
async def get_training_data(days: int = 30):
    """Get AI training data"""
    data = await db.get_ai_training_data(days)
    return {"success": True, "data": data}

@app.get("/api/ai/device-pattern/{device_id}")
async def get_device_pattern(device_id: str):
    """Get device usage pattern"""
    pattern = await db.get_device_usage_pattern(device_id)
    return {"success": True, "data": pattern}

# ==================== STATISTICS ENDPOINTS ====================

@app.get("/api/stats/devices")
async def get_device_stats():
    """Get device statistics"""
    stats = await db.get_device_statistics()
    return {"success": True, "data": stats}

@app.get("/api/stats/system")
async def get_system_stats():
    """Get overall system statistics"""
    devices = await db.get_all_devices()
    active_devices = sum(1 for d in devices if d['status'] == 1)
    
    energy = await db.get_energy_report(1)
    alerts = await db.get_unresolved_alerts()
    
    return {
        "success": True,
        "data": {
            "total_devices": len(devices),
            "active_devices": active_devices,
            "energy_today_kwh": energy.get('total_kwh', 0),
            "unresolved_alerts": len(alerts),
            "timestamp": datetime.now().isoformat()
        }
    }

# ==================== HARDWARE ENDPOINTS ====================

@app.post("/api/hardware/register")
async def register_hardware(device_id: str, hardware_id: str, device_type: str):
    """Register hardware device (ESP32, Arduino, etc.)"""
    # Store hardware mapping
    return {
        "success": True,
        "message": f"Hardware {hardware_id} registered for {device_id}",
        "mqtt_topic": f"smarthome/{device_id}/command"
    }

@app.get("/api/hardware/status")
async def get_hardware_status():
    """Get status of all connected hardware"""
    # Return list of connected hardware devices
    return {
        "success": True,
        "data": {
            "connected_devices": mqtt.get_connected_devices(),
            "mqtt_status": "connected" if mqtt.is_connected() else "disconnected"
        }
    }

# ==================== HEALTH CHECK ====================

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "services": {
            "database": "connected",
            "mqtt": "connected" if mqtt.is_connected() else "disconnected",
            "websocket": f"{len(ws_manager.active_connections)} clients"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
