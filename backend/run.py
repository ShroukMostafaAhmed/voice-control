#!/usr/bin/env python3
"""
Run Smart Home Backend Server
"""

import uvicorn
import sys
import os

# Add parent directory to path for database access
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

if __name__ == "__main__":
    print("=" * 50)
    print("Smart Home Backend Server")
    print("=" * 50)
    print("\nStarting services...")
    print("   - API Server: http://localhost:8080")
    print("   - WebSocket: ws://localhost:8080/ws")
    print("   - MQTT Broker: localhost:1883")
    print("\nMake sure MQTT broker is running:")
    print("   Windows: Download Mosquitto from mosquitto.org")
    print("   Linux: sudo apt-get install mosquitto")
    print("   Mac: brew install mosquitto")
    print("\n" + "=" * 50 + "\n")
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8080,
        reload=True,
        log_level="info"
    )
