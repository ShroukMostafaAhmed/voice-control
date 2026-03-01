"""
MQTT Manager for Hardware Communication
Supports ESP32, Arduino, Raspberry Pi, etc.
"""

import paho.mqtt.client as mqtt
import json
import asyncio
from typing import Dict, Callable, List

class MQTTManager:
    def __init__(self, broker="localhost", port=1883):
        self.broker = broker
        self.port = port
        self.client = None
        self.connected = False
        self.connected_devices = []
        self.message_callbacks = []
    
    async def connect(self):
        """Connect to MQTT broker"""
        self.client = mqtt.Client(client_id="smarthome_backend")
        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message
        self.client.on_disconnect = self._on_disconnect
        
        try:
            self.client.connect(self.broker, self.port, 60)
            self.client.loop_start()
            print(f"✓ MQTT connected to {self.broker}:{self.port}")
        except Exception as e:
            print(f"✗ MQTT connection failed: {e}")
            print("  Note: Install Mosquitto MQTT broker or use cloud MQTT")
    
    async def disconnect(self):
        """Disconnect from MQTT broker"""
        if self.client:
            self.client.loop_stop()
            self.client.disconnect()
    
    def _on_connect(self, client, userdata, flags, rc):
        """Callback when connected to MQTT broker"""
        if rc == 0:
            self.connected = True
            print("✓ MQTT broker connected")
            
            # Subscribe to all device topics
            client.subscribe("smarthome/+/status")  # Device status updates
            client.subscribe("smarthome/+/sensor")  # Sensor data
            client.subscribe("smarthome/hardware/+/register")  # Hardware registration
        else:
            print(f"✗ MQTT connection failed with code {rc}")
    
    def _on_disconnect(self, client, userdata, rc):
        """Callback when disconnected from MQTT broker"""
        self.connected = False
        print("✗ MQTT broker disconnected")
    
    def _on_message(self, client, userdata, msg):
        """Callback when message received from MQTT"""
        try:
            topic = msg.topic
            payload = json.loads(msg.payload.decode())
            
            print(f"📨 MQTT: {topic} -> {payload}")
            
            # Handle different message types
            if "/status" in topic:
                self._handle_device_status(topic, payload)
            elif "/sensor" in topic:
                self._handle_sensor_data(topic, payload)
            elif "/register" in topic:
                self._handle_hardware_register(topic, payload)
            
            # Call registered callbacks
            for callback in self.message_callbacks:
                asyncio.create_task(callback(topic, payload))
                
        except Exception as e:
            print(f"✗ MQTT message error: {e}")
    
    def _handle_device_status(self, topic: str, payload: Dict):
        """Handle device status update from hardware"""
        device_id = topic.split('/')[1]
        status = payload.get('status', 0)
        print(f"  Device {device_id} status: {status}")
    
    def _handle_sensor_data(self, topic: str, payload: Dict):
        """Handle sensor data from hardware"""
        device_id = topic.split('/')[1]
        sensor_type = payload.get('type')
        value = payload.get('value')
        print(f"  Sensor {device_id} ({sensor_type}): {value}")
    
    def _handle_hardware_register(self, topic: str, payload: Dict):
        """Handle hardware device registration"""
        hardware_id = payload.get('hardware_id')
        device_type = payload.get('device_type')
        
        if hardware_id not in self.connected_devices:
            self.connected_devices.append(hardware_id)
            print(f"  Hardware registered: {hardware_id} ({device_type})")
    
    async def publish_device_command(self, device_id: str, status: int):
        """Publish command to device (to hardware)"""
        if not self.connected:
            print("WARNING: MQTT not connected, command not sent")
            return
        
        topic = f"smarthome/{device_id}/command"
        payload = json.dumps({
            "status": status,
            "timestamp": asyncio.get_event_loop().time()
        })
        
        self.client.publish(topic, payload)
        print(f"📤 MQTT: {topic} -> status={status}")
    
    async def publish_sensor_request(self, device_id: str, sensor_type: str):
        """Request sensor reading from hardware"""
        if not self.connected:
            return
        
        topic = f"smarthome/{device_id}/request"
        payload = json.dumps({"type": sensor_type})
        
        self.client.publish(topic, payload)
    
    def register_callback(self, callback: Callable):
        """Register callback for MQTT messages"""
        self.message_callbacks.append(callback)
    
    def is_connected(self) -> bool:
        """Check if MQTT is connected"""
        return self.connected
    
    def get_connected_devices(self) -> List[str]:
        """Get list of connected hardware devices"""
        return self.connected_devices


# MQTT Topics Structure:
# 
# Commands (Backend -> Hardware):
#   smarthome/{device_id}/command     - Control device (ON/OFF)
#   smarthome/{device_id}/request     - Request sensor reading
#
# Status (Hardware -> Backend):
#   smarthome/{device_id}/status      - Device status update
#   smarthome/{device_id}/sensor      - Sensor data
#   smarthome/hardware/{id}/register  - Hardware registration
#
# Example Hardware Code (ESP32/Arduino):
# 
# void setup() {
#   mqtt.subscribe("smarthome/light1/command");
# }
# 
# void callback(char* topic, byte* payload, unsigned int length) {
#   if (strcmp(topic, "smarthome/light1/command") == 0) {
#     int status = payload[0] - '0';
#     digitalWrite(LED_PIN, status);
#     
#     // Send status back
#     mqtt.publish("smarthome/light1/status", "{\"status\": 1}");
#   }
# }
