"""
Smart Home Data Generator
Generates large CSV dataset for AI model training
Includes realistic scenarios, dangers, and device patterns
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import csv

class SmartHomeDataGenerator:
    def __init__(self):
        # All devices in the smart home
        self.devices = [
            'bath_light', 'bath_heater', 'bath_fan',
            'corr_main_light', 'corr_spots',
            'rec_light', 'rec_window', 'rec_sound', 'rec_ac',
            'out_camera', 'out_light', 'out_door',
            'r1_ac', 'r1_tv', 'r1_light', 'r1_window', 'r1_sound',
            'kit_light', 'kit_window', 'kit_fan',
            'r2_ac', 'r2_sound', 'r2_light'
        ]
        
        # Device types for energy calculation
        self.device_types = {
            'light': ['bath_light', 'corr_main_light', 'corr_spots', 'rec_light', 
                     'out_light', 'r1_light', 'kit_light', 'r2_light'],
            'ac': ['rec_ac', 'r1_ac', 'r2_ac'],
            'heater': ['bath_heater'],
            'fan': ['bath_fan', 'kit_fan'],
            'window': ['rec_window', 'r1_window', 'kit_window'],
            'sound': ['rec_sound', 'r1_sound', 'r2_sound'],
            'tv': ['r1_tv'],
            'camera': ['out_camera'],
            'door': ['out_door']
        }
        
        # Rooms mapping
        self.device_rooms = {
            'bathroom': ['bath_light', 'bath_heater', 'bath_fan'],
            'corridors': ['corr_main_light', 'corr_spots'],
            'reception': ['rec_light', 'rec_window', 'rec_sound', 'rec_ac'],
            'outdoor': ['out_camera', 'out_light', 'out_door'],
            'room1': ['r1_ac', 'r1_tv', 'r1_light', 'r1_window', 'r1_sound'],
            'kitchen': ['kit_light', 'kit_window', 'kit_fan'],
            'room2': ['r2_ac', 'r2_sound', 'r2_light']
        }
    
    def generate_dataset(self, num_samples=50000, output_file='training_data.csv'):
        """Generate large training dataset with realistic scenarios"""
        print(f"🔄 Generating {num_samples:,} training samples...")
        
        data = []
        start_date = datetime.now() - timedelta(days=365)  # 1 year of data
        
        for i in range(num_samples):
            if i % 5000 == 0:
                print(f"   Progress: {i:,}/{num_samples:,} ({i*100//num_samples}%)")
            
            # Generate timestamp
            timestamp = start_date + timedelta(minutes=random.randint(0, 525600))
            hour = timestamp.hour
            day_of_week = timestamp.weekday()
            month = timestamp.month
            
            # Generate sensor data
            sensors = self._generate_sensor_data(hour, month)
            
            # Generate device states based on scenarios
            device_states = self._generate_device_states(hour, day_of_week, sensors)
            
            # Create row
            row = {
                'timestamp': timestamp.isoformat(),
                'hour': hour,
                'day_of_week': day_of_week,
                'month': month,
                'is_weekend': 1 if day_of_week >= 5 else 0,
                'temperature': sensors['temperature'],
                'humidity': sensors['humidity'],
                'motion_detected': sensors['motion'],
                'light_level': sensors['light_level'],
                'smoke_detected': sensors['smoke'],
                'user_present': sensors['user_present'],
                'outdoor_temp': sensors['outdoor_temp'],
                'rain': sensors['rain'],
                'scenario': sensors['scenario'],
                'danger_level': sensors['danger_level']
            }
            
            # Add device states
            for device in self.devices:
                row[f'{device}_status'] = device_states.get(device, 0)
            
            # Add recommended actions
            row['recommended_action'] = sensors['recommended_action']
            row['action_priority'] = sensors['action_priority']
            
            data.append(row)
        
        # Create DataFrame
        df = pd.DataFrame(data)
        
        # Save to CSV
        df.to_csv(output_file, index=False)
        print(f"\n✅ Dataset saved: {output_file}")
        print(f"   Total samples: {len(df):,}")
        print(f"   File size: {df.memory_usage(deep=True).sum() / 1024 / 1024:.2f} MB")
        print(f"   Columns: {len(df.columns)}")
        
        # Print statistics
        self._print_statistics(df)
        
        return df
    
    def _generate_sensor_data(self, hour, month):
        """Generate realistic sensor data with scenarios"""
        
        # Base temperature (varies by month and hour)
        base_temp = 20 + (month - 6) * 2  # Warmer in summer
        if 6 <= hour <= 18:
            base_temp += random.uniform(2, 5)  # Warmer during day
        temperature = base_temp + random.uniform(-3, 3)
        temperature = max(15, min(40, temperature))
        
        # Humidity (higher in bathroom, kitchen)
        humidity = random.uniform(35, 65)
        
        # Motion detection (higher during day, weekdays)
        motion_prob = 0.7 if 7 <= hour <= 22 else 0.2
        motion = 1 if random.random() < motion_prob else 0
        
        # Light level (depends on time)
        if 6 <= hour <= 18:
            light_level = random.uniform(300, 800)
        else:
            light_level = random.uniform(10, 100)
        
        # User present (higher during evening/night)
        user_prob = 0.9 if 18 <= hour <= 23 or 0 <= hour <= 7 else 0.3
        user_present = 1 if random.random() < user_prob else 0
        
        # Outdoor temperature
        outdoor_temp = temperature + random.uniform(-5, 5)
        
        # Rain
        rain = 1 if random.random() < 0.15 else 0
        
        # Determine scenario and danger level
        scenario, danger_level, smoke, recommended_action, priority = self._determine_scenario(
            temperature, humidity, motion, light_level, hour, user_present, outdoor_temp
        )
        
        return {
            'temperature': round(temperature, 1),
            'humidity': round(humidity, 1),
            'motion': motion,
            'light_level': round(light_level, 0),
            'smoke': smoke,
            'user_present': user_present,
            'outdoor_temp': round(outdoor_temp, 1),
            'rain': rain,
            'scenario': scenario,
            'danger_level': danger_level,
            'recommended_action': recommended_action,
            'action_priority': priority
        }
    
    def _determine_scenario(self, temp, humidity, motion, light, hour, user_present, outdoor_temp):
        """Determine scenario and recommended actions"""
        
        # DANGER SCENARIOS (High Priority)
        
        # Fire/Smoke (1% chance)
        if random.random() < 0.01:
            return ('fire_emergency', 'critical', 1, 'open_all_windows_alert', 10)
        
        # Extreme heat (>35°C)
        if temp > 35:
            return ('extreme_heat', 'high', 0, 'turn_on_all_ac_open_windows', 9)
        
        # Gas leak simulation (high humidity + no motion + night)
        if humidity > 70 and motion == 0 and 0 <= hour <= 5:
            if random.random() < 0.005:
                return ('possible_gas_leak', 'high', 0, 'open_windows_alert', 9)
        
        # Intrusion (motion at night + user not present)
        if motion == 1 and 0 <= hour <= 5 and user_present == 0:
            if random.random() < 0.02:
                return ('intrusion_detected', 'high', 0, 'alert_turn_on_all_lights', 8)
        
        # NORMAL SCENARIOS
        
        # Morning routine (7-9 AM, weekdays)
        if 7 <= hour <= 9 and user_present == 1:
            return ('morning_routine', 'normal', 0, 'turn_on_bathroom_kitchen_lights', 5)
        
        # High temperature + user present
        if temp > 28 and user_present == 1:
            return ('hot_weather', 'normal', 0, 'turn_on_ac', 6)
        
        # Low temperature
        if temp < 18:
            return ('cold_weather', 'normal', 0, 'turn_on_heater', 5)
        
        # Night mode (after 10 PM)
        if hour >= 22 and user_present == 1:
            return ('night_mode', 'normal', 0, 'dim_lights_turn_off_tv', 4)
        
        # No motion for long time
        if motion == 0 and light < 100:
            return ('no_activity', 'normal', 0, 'turn_off_lights', 3)
        
        # Dark room + motion
        if light < 100 and motion == 1:
            return ('dark_room_activity', 'normal', 0, 'turn_on_lights', 5)
        
        # High humidity (bathroom usage)
        if humidity > 65:
            return ('high_humidity', 'normal', 0, 'turn_on_fan', 4)
        
        # Energy saving mode (no user)
        if user_present == 0:
            return ('energy_saving', 'normal', 0, 'turn_off_non_essential', 3)
        
        # Rain detected
        if outdoor_temp < temp - 5:
            return ('rain_weather', 'normal', 0, 'close_windows', 4)
        
        # Default
        return ('normal_operation', 'low', 0, 'maintain_current_state', 1)
    
    def _generate_device_states(self, hour, day_of_week, sensors):
        """Generate device states based on scenario"""
        states = {}
        scenario = sensors['scenario']
        temp = sensors['temperature']
        motion = sensors['motion']
        user_present = sensors['user_present']
        light_level = sensors['light_level']
        smoke = sensors['smoke']
        
        # Initialize all devices to OFF
        for device in self.devices:
            states[device] = 0
        
        # Camera always ON
        states['out_camera'] = 1
        
        # DANGER SCENARIOS
        
        if scenario == 'fire_emergency':
            # Open all windows
            for device in self.device_types['window']:
                states[device] = 1
            # Turn on all lights for visibility
            for device in self.device_types['light']:
                states[device] = 1
            return states
        
        if scenario == 'extreme_heat':
            # Turn on all ACs
            for device in self.device_types['ac']:
                states[device] = 1
            # Open windows
            for device in self.device_types['window']:
                states[device] = 1
            return states
        
        if scenario == 'possible_gas_leak':
            # Open all windows
            for device in self.device_types['window']:
                states[device] = 1
            # Turn on fans
            for device in self.device_types['fan']:
                states[device] = 1
            return states
        
        if scenario == 'intrusion_detected':
            # Turn on all lights
            for device in self.device_types['light']:
                states[device] = 1
            # Turn on outdoor light
            states['out_light'] = 1
            return states
        
        # NORMAL SCENARIOS
        
        if scenario == 'morning_routine':
            states['bath_light'] = 1
            states['kit_light'] = 1
            states['corr_main_light'] = 1
            if temp < 20:
                states['bath_heater'] = 1
        
        elif scenario == 'hot_weather':
            if user_present:
                # Turn on AC in occupied rooms
                states['rec_ac'] = 1
                if motion:
                    states['r1_ac'] = 1
        
        elif scenario == 'cold_weather':
            states['bath_heater'] = 1
            # Close windows
            for device in self.device_types['window']:
                states[device] = 0
        
        elif scenario == 'night_mode':
            # Dim lights (only bedroom)
            states['r1_light'] = 1
            states['r2_light'] = 1
            # Turn off TV
            states['r1_tv'] = 0
            # Turn off sound systems
            for device in self.device_types['sound']:
                states[device] = 0
        
        elif scenario == 'no_activity':
            # Turn off most lights
            for device in self.device_types['light']:
                if device != 'out_light':  # Keep outdoor light
                    states[device] = 0
        
        elif scenario == 'dark_room_activity':
            # Turn on lights where motion detected
            if motion:
                states['corr_main_light'] = 1
                states['rec_light'] = 1
        
        elif scenario == 'high_humidity':
            states['bath_fan'] = 1
            states['kit_fan'] = 1
        
        elif scenario == 'energy_saving':
            # Turn off non-essential devices
            for device in self.device_types['sound']:
                states[device] = 0
            for device in self.device_types['tv']:
                states[device] = 0
        
        elif scenario == 'rain_weather':
            # Close windows
            for device in self.device_types['window']:
                states[device] = 0
        
        # Add some randomness for realism
        if user_present and random.random() < 0.3:
            # Random device usage
            random_device = random.choice(self.devices)
            states[random_device] = random.choice([0, 1])
        
        return states
    
    def _print_statistics(self, df):
        """Print dataset statistics"""
        print("\n📊 Dataset Statistics:")
        print(f"   Scenarios distribution:")
        for scenario, count in df['scenario'].value_counts().head(10).items():
            print(f"      {scenario}: {count:,} ({count*100/len(df):.1f}%)")
        
        print(f"\n   Danger levels:")
        for level, count in df['danger_level'].value_counts().items():
            print(f"      {level}: {count:,} ({count*100/len(df):.1f}%)")
        
        print(f"\n   Temperature range: {df['temperature'].min():.1f}°C - {df['temperature'].max():.1f}°C")
        print(f"   Average temperature: {df['temperature'].mean():.1f}°C")
        print(f"   Motion detected: {df['motion_detected'].sum():,} times ({df['motion_detected'].mean()*100:.1f}%)")
        print(f"   Smoke detected: {df['smoke_detected'].sum():,} times ({df['smoke_detected'].mean()*100:.1f}%)")


if __name__ == "__main__":
    print("=" * 70)
    print("Smart Home AI Training Data Generator")
    print("=" * 70)
    print()
    
    generator = SmartHomeDataGenerator()
    
    # Generate 50,000 samples (you can increase this)
    df = generator.generate_dataset(num_samples=50000, output_file='training_data.csv')
    
    print("\n✅ Data generation complete!")
    print("   Next step: Run 'python train_model.py' to train the AI model")
