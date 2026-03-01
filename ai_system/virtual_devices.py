"""
Virtual Smart Home Devices
Simulates real hardware devices
"""

import random
from datetime import datetime
from typing import Dict, List

class Device:
    """Base device class"""
    def __init__(self, device_id: str, name: str, room: str, device_type: str):
        self.device_id = device_id
        self.name = name
        self.room = room
        self.type = device_type
        self.state = 0  # 0 = OFF, 1 = ON
        self.last_updated = datetime.now()
    
    def turn_on(self):
        """Turn device on"""
        self.state = 1
        self.last_updated = datetime.now()
        return True
    
    def turn_off(self):
        """Turn device off"""
        self.state = 0
        self.last_updated = datetime.now()
        return True
    
    def toggle(self):
        """Toggle device state"""
        self.state = 1 if self.state == 0 else 0
        self.last_updated = datetime.now()
        return self.state
    
    def get_state(self) -> Dict:
        """Get device state"""
        return {
            'device_id': self.device_id,
            'name': self.name,
            'room': self.room,
            'type': self.type,
            'state': self.state,
            'last_updated': self.last_updated.isoformat()
        }


class Sensor(Device):
    """Sensor device with value reading"""
    def __init__(self, device_id: str, name: str, room: str, sensor_type: str):
        super().__init__(device_id, name, room, sensor_type)
        self.value = 0
        self.unit = self._get_unit()
    
    def _get_unit(self) -> str:
        """Get unit based on sensor type"""
        units = {
            'temperature': '°C',
            'humidity': '%',
            'motion': '',
            'smoke': '',
            'light': 'lux'
        }
        return units.get(self.type, '')
    
    def read_value(self) -> float:
        """Read sensor value (simulated)"""
        self.value = self._generate_value()
        self.last_updated = datetime.now()
        return self.value
    
    def _generate_value(self) -> float:
        """Generate fake sensor data"""
        if self.type == 'temperature':
            # Temperature between 18-35°C
            return round(random.uniform(18, 35), 1)
        
        elif self.type == 'humidity':
            # Humidity between 30-70%
            return round(random.uniform(30, 70), 1)
        
        elif self.type == 'motion':
            # Motion detected or not
            return random.choice([0, 1])
        
        elif self.type == 'smoke':
            # Smoke detected (rare)
            return 1 if random.random() > 0.98 else 0
        
        elif self.type == 'light':
            # Light level 0-1000 lux
            hour = datetime.now().hour
            if 6 <= hour <= 18:
                return round(random.uniform(300, 800), 0)
            else:
                return round(random.uniform(10, 100), 0)
        
        return 0
    
    def get_state(self) -> Dict:
        """Get sensor state with value"""
        state = super().get_state()
        state['value'] = self.value
        state['unit'] = self.unit
        return state


class VirtualSmartHome:
    """Virtual Smart Home with all devices"""
    def __init__(self):
        self.devices: Dict[str, Device] = {}
        self.sensors: Dict[str, Sensor] = {}
        self._initialize_devices()
    
    def _initialize_devices(self):
        """Initialize all virtual devices"""
        # Bathroom
        self.devices['bath_light'] = Device('bath_light', 'Light System', 'bathroom', 'light')
        self.devices['bath_heater'] = Device('bath_heater', 'Water Heater', 'bathroom', 'heater')
        self.devices['bath_fan'] = Device('bath_fan', 'Fan System', 'bathroom', 'fan')
        self.sensors['bath_fire'] = Sensor('bath_fire', 'Fire Alert', 'bathroom', 'smoke')
        
        # Corridors
        self.devices['corr_main_light'] = Device('corr_main_light', 'Main Light', 'corridors', 'light')
        self.devices['corr_spots'] = Device('corr_spots', 'Spots Light', 'corridors', 'light')
        self.sensors['corr_fire'] = Sensor('corr_fire', 'Fire Alert', 'corridors', 'smoke')
        
        # Reception
        self.devices['rec_light'] = Device('rec_light', 'Light System', 'reception', 'light')
        self.devices['rec_window'] = Device('rec_window', 'Smart Window', 'reception', 'window')
        self.devices['rec_sound'] = Device('rec_sound', 'Sound System', 'reception', 'sound')
        self.devices['rec_ac'] = Device('rec_ac', 'Air Condition', 'reception', 'ac')
        self.sensors['rec_fire'] = Sensor('rec_fire', 'Fire Alert', 'reception', 'smoke')
        
        # Outdoor
        self.devices['out_camera'] = Device('out_camera', 'Camera System', 'outdoor', 'camera')
        self.devices['out_light'] = Device('out_light', 'Light System', 'outdoor', 'light')
        self.devices['out_door'] = Device('out_door', 'Smart Door', 'outdoor', 'door')
        
        # Room 1
        self.devices['r1_ac'] = Device('r1_ac', 'Air Condition', 'room1', 'ac')
        self.devices['r1_tv'] = Device('r1_tv', 'TV', 'room1', 'tv')
        self.devices['r1_light'] = Device('r1_light', 'Light System', 'room1', 'light')
        self.devices['r1_window'] = Device('r1_window', 'Smart Window', 'room1', 'window')
        self.devices['r1_sound'] = Device('r1_sound', 'Sound System', 'room1', 'sound')
        self.sensors['r1_fire'] = Sensor('r1_fire', 'Fire Alert', 'room1', 'smoke')
        
        # Kitchen
        self.devices['kit_light'] = Device('kit_light', 'Light System', 'kitchen', 'light')
        self.devices['kit_window'] = Device('kit_window', 'Smart Window', 'kitchen', 'window')
        self.devices['kit_fan'] = Device('kit_fan', 'Fan System', 'kitchen', 'fan')
        self.sensors['kit_fire'] = Sensor('kit_fire', 'Fire Alert', 'kitchen', 'smoke')
        
        # Room 2
        self.devices['r2_ac'] = Device('r2_ac', 'Air Condition', 'room2', 'ac')
        self.devices['r2_sound'] = Device('r2_sound', 'Sound System', 'room2', 'sound')
        self.devices['r2_light'] = Device('r2_light', 'Light System', 'room2', 'light')
        self.sensors['r2_fire'] = Sensor('r2_fire', 'Fire Alert', 'room2', 'smoke')
        
        # Environmental sensors
        self.sensors['temp_reception'] = Sensor('temp_reception', 'Temperature', 'reception', 'temperature')
        self.sensors['humidity_bathroom'] = Sensor('humidity_bathroom', 'Humidity', 'bathroom', 'humidity')
        self.sensors['motion_corridors'] = Sensor('motion_corridors', 'Motion', 'corridors', 'motion')
        self.sensors['light_reception'] = Sensor('light_reception', 'Light Level', 'reception', 'light')
        
        # Turn on camera by default
        self.devices['out_camera'].turn_on()
    
    def get_device(self, device_id: str) -> Device:
        """Get device by ID"""
        return self.devices.get(device_id) or self.sensors.get(device_id)
    
    def get_all_devices(self) -> List[Dict]:
        """Get all devices state"""
        all_devices = []
        for device in self.devices.values():
            all_devices.append(device.get_state())
        for sensor in self.sensors.values():
            all_devices.append(sensor.get_state())
        return all_devices
    
    def get_room_devices(self, room: str) -> List[Dict]:
        """Get devices in a room"""
        room_devices = []
        for device in self.devices.values():
            if device.room == room:
                room_devices.append(device.get_state())
        for sensor in self.sensors.values():
            if sensor.room == room:
                room_devices.append(sensor.get_state())
        return room_devices
    
    def control_device(self, device_id: str, action: str) -> Dict:
        """Control a device"""
        device = self.get_device(device_id)
        if not device:
            return {'success': False, 'message': f'Device {device_id} not found'}
        
        if action == 'on':
            device.turn_on()
        elif action == 'off':
            device.turn_off()
        elif action == 'toggle':
            device.toggle()
        else:
            return {'success': False, 'message': f'Unknown action: {action}'}
        
        return {
            'success': True,
            'device_id': device_id,
            'state': device.state,
            'message': f'{device.name} turned {"ON" if device.state == 1 else "OFF"}'
        }
    
    def read_all_sensors(self) -> Dict[str, float]:
        """Read all sensors"""
        readings = {}
        for sensor_id, sensor in self.sensors.items():
            readings[sensor_id] = sensor.read_value()
        return readings
    
    def get_environment_data(self) -> Dict:
        """Get current environment data"""
        return {
            'temperature': self.sensors['temp_reception'].read_value(),
            'humidity': self.sensors['humidity_bathroom'].read_value(),
            'motion': self.sensors['motion_corridors'].read_value(),
            'light_level': self.sensors['light_reception'].read_value(),
            'timestamp': datetime.now().isoformat()
        }


# Global instance
virtual_home = VirtualSmartHome()
