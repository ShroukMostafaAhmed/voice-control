"""
AI Decision Engine
Rule-based + ML hybrid system
"""

import random
from datetime import datetime
from typing import Dict, List, Tuple
import json

class AIEngine:
    """AI Engine for smart home automation"""
    
    def __init__(self):
        self.rules = self._initialize_rules()
        self.learning_data = []
        self.decisions_log = []
        self.auto_mode = False  # Auto control mode
    
    def _initialize_rules(self) -> List[Dict]:
        """Initialize automation rules"""
        return [
            {
                'name': 'High Temperature AC',
                'condition': lambda env: env['temperature'] > 28 and env['motion'] == 1,
                'action': 'turn_on_ac',
                'priority': 10,
                'devices': ['rec_ac', 'r1_ac', 'r2_ac']
            },
            {
                'name': 'Low Temperature AC Off',
                'condition': lambda env: env['temperature'] < 24,
                'action': 'turn_off_ac',
                'priority': 8,
                'devices': ['rec_ac', 'r1_ac', 'r2_ac']
            },
            {
                'name': 'No Motion Lights Off',
                'condition': lambda env: env['motion'] == 0,
                'action': 'turn_off_lights',
                'priority': 5,
                'devices': ['corr_main_light', 'corr_spots']
            },
            {
                'name': 'Motion Detected Lights On',
                'condition': lambda env: env['motion'] == 1,
                'action': 'turn_on_lights',
                'priority': 7,
                'devices': ['corr_main_light', 'corr_spots']
            },
            {
                'name': 'Night Mode',
                'condition': lambda env: env['hour'] >= 22 or env['hour'] <= 6,
                'action': 'night_mode',
                'priority': 6,
                'devices': ['rec_light', 'kit_light']
            },
            {
                'name': 'Morning Routine',
                'condition': lambda env: env['hour'] == 7 and env['day_of_week'] < 5,
                'action': 'morning_routine',
                'priority': 9,
                'devices': ['bath_light', 'kit_light']
            },
            {
                'name': 'Fire Emergency',
                'condition': lambda env: env.get('smoke_detected', 0) == 1,
                'action': 'fire_emergency',
                'priority': 100,
                'devices': ['rec_window', 'kit_window', 'r1_window']
            },
            {
                'name': 'Dark Room Lights On',
                'condition': lambda env: env['light_level'] < 100 and env['motion'] == 1,
                'action': 'turn_on_lights',
                'priority': 7,
                'devices': ['rec_light']
            }
        ]
    
    def analyze_environment(self, env_data: Dict) -> Dict:
        """Analyze environment and make decisions"""
        now = datetime.now()
        
        # Add time context
        env_data['hour'] = now.hour
        env_data['day_of_week'] = now.weekday()
        
        # Check all rules
        triggered_rules = []
        for rule in sorted(self.rules, key=lambda x: x['priority'], reverse=True):
            try:
                if rule['condition'](env_data):
                    triggered_rules.append(rule)
            except Exception as e:
                print(f"Rule error: {rule['name']} - {e}")
        
        return {
            'triggered_rules': triggered_rules,
            'environment': env_data,
            'timestamp': now.isoformat()
        }
    
    def make_decision(self, env_data: Dict) -> List[Dict]:
        """Make AI decisions based on environment"""
        analysis = self.analyze_environment(env_data)
        actions = []
        
        for rule in analysis['triggered_rules']:
            action = {
                'rule': rule['name'],
                'action': rule['action'],
                'devices': rule['devices'],
                'priority': rule['priority'],
                'reason': self._get_reason(rule, env_data)
            }
            actions.append(action)
        
        # Log decision
        self.decisions_log.append({
            'timestamp': datetime.now().isoformat(),
            'environment': env_data,
            'actions': actions
        })
        
        # Keep only last 100 decisions
        if len(self.decisions_log) > 100:
            self.decisions_log = self.decisions_log[-100:]
        
        return actions
    
    def _get_reason(self, rule: Dict, env_data: Dict) -> str:
        """Generate human-readable reason"""
        reasons = {
            'turn_on_ac': f"Temperature is {env_data['temperature']}°C (high)",
            'turn_off_ac': f"Temperature is {env_data['temperature']}°C (comfortable)",
            'turn_off_lights': "No motion detected",
            'turn_on_lights': "Motion detected" if env_data['motion'] else f"Light level is {env_data.get('light_level', 0)} lux (dark)",
            'night_mode': f"Night time ({env_data['hour']}:00)",
            'morning_routine': "Morning routine activated",
            'fire_emergency': "FIRE DETECTED - Emergency protocol"
        }
        return reasons.get(rule['action'], rule['name'])
    
    def execute_actions(self, actions: List[Dict], virtual_home) -> List[Dict]:
        """Execute AI decisions on virtual home"""
        results = []
        
        for action in actions:
            action_type = action['action']
            devices = action['devices']
            
            for device_id in devices:
                if action_type == 'turn_on_ac':
                    result = virtual_home.control_device(device_id, 'on')
                elif action_type == 'turn_off_ac':
                    result = virtual_home.control_device(device_id, 'off')
                elif action_type == 'turn_on_lights':
                    result = virtual_home.control_device(device_id, 'on')
                elif action_type == 'turn_off_lights':
                    result = virtual_home.control_device(device_id, 'off')
                elif action_type == 'night_mode':
                    result = virtual_home.control_device(device_id, 'off')
                elif action_type == 'morning_routine':
                    result = virtual_home.control_device(device_id, 'on')
                elif action_type == 'fire_emergency':
                    result = virtual_home.control_device(device_id, 'on')
                else:
                    continue
                
                result['rule'] = action['rule']
                result['reason'] = action['reason']
                results.append(result)
        
        return results
    
    def process_command(self, command: str, virtual_home) -> Dict:
        """Process natural language command with dynamic support"""
        original_command = command
        command = command.lower()
        
        # Check for dynamic commands (all, everything, etc.)
        if self._is_dynamic_command(command):
            return self._process_dynamic_command(command, virtual_home, original_command)
        
        # Parse command
        if 'turn on' in command or 'switch on' in command or 'open' in command or 'enable' in command or 'start' in command:
            action = 'on'
        elif 'turn off' in command or 'switch off' in command or 'close' in command or 'disable' in command or 'stop' in command:
            action = 'off'
        else:
            return {
                'success': False,
                'message': "I didn't understand the command. Try 'turn on' or 'turn off'",
                'command': original_command
            }
        
        # Enhanced device keywords with more variations
        device_keywords = {
            'light': ['light', 'lights', 'lamp', 'lighting', 'bulb'],
            'ac': ['ac', 'air condition', 'air conditioning', 'cooling', 'conditioner'],
            'tv': ['tv', 'television', 'telly'],
            'fan': ['fan', 'ventilator'],
            'window': ['window', 'windows'],
            'door': ['door', 'gate', 'entrance'],
            'sound': ['sound', 'speaker', 'music', 'audio', 'speakers'],
            'camera': ['camera', 'cam', 'cctv', 'surveillance'],
            'heater': ['heater', 'water heater', 'heating'],
            'spots': ['spots', 'spot lights', 'spotlights'],
            'fire': ['fire', 'fire alert', 'smoke', 'smoke detector', 'fire alarm']
        }
        
        # Enhanced room keywords with more variations
        room_keywords = {
            'reception': ['reception', 'living room', 'hall', 'living', 'rec'],
            'bathroom': ['bathroom', 'bath', 'toilet', 'washroom'],
            'kitchen': ['kitchen', 'kit'],
            'room1': ['room 1', 'room1', 'r1', 'bedroom 1', 'first room', 'room one', 'bedroom one'],
            'room2': ['room 2', 'room2', 'r2', 'bedroom 2', 'second room', 'room two', 'bedroom two'],
            'corridors': ['corridor', 'hallway', 'corr', 'corridors', 'passage', 'hall way'],
            'outdoor': ['outdoor', 'outside', 'garden', 'out door', 'out', 'exterior', 'outdoors']
        }
        
        # Find device type - prioritize earlier matches
        device_type = None
        device_position = 999
        
        for dtype, keywords in device_keywords.items():
            for kw in keywords:
                if kw in command:
                    pos = command.index(kw)
                    # Prioritize device type mentioned first
                    if pos < device_position:
                        device_type = dtype
                        device_position = pos
                        break
        
        # Find room - prioritize earlier matches
        room = None
        room_position = 999
        
        for room_name, keywords in room_keywords.items():
            for kw in keywords:
                if kw in command:
                    pos = command.index(kw)
                    # Prioritize room mentioned first
                    if pos < room_position:
                        room = room_name
                        room_position = pos
                        break
        
        # Build device ID with comprehensive mapping
        device_id = None
        
        if device_type and room:
            # Map room names to prefixes
            room_prefix_map = {
                'reception': 'rec',
                'bathroom': 'bath',
                'kitchen': 'kit',
                'room1': 'r1',
                'room2': 'r2',
                'corridors': 'corr',
                'outdoor': 'out'
            }
            
            prefix = room_prefix_map.get(room, room)
            
            # Try multiple device ID patterns
            possible_ids = [
                f"{prefix}_{device_type}",
                f"{room}_{device_type}",
            ]
            
            # Special cases for specific devices
            if device_type == 'light' and room == 'corridors':
                possible_ids.extend(['corr_main_light', 'corr_spots'])
            
            # Try to find the device
            for pid in possible_ids:
                if virtual_home.get_device(pid):
                    device_id = pid
                    break
        
        elif device_type:
            # Find first device of this type
            for dev_id, device in virtual_home.devices.items():
                if device_type in dev_id:
                    device_id = dev_id
                    break
        
        # If still not found, try fuzzy matching
        if not device_id:
            all_devices = virtual_home.get_all_devices()
            
            # Try to match by device name or type
            for device in all_devices:
                dev_id = device['device_id']
                dev_name = device['name'].lower()
                dev_type = device['type'].lower()
                
                # Check if command contains device name or type
                if (device_type and device_type in dev_id) or \
                   (room and any(r in dev_id for r in [room, room_keywords.get(room, [''])[0]])):
                    device_id = dev_id
                    break
        
        if not device_id:
            # List available devices for better error message
            available = []
            if room:
                room_devices = virtual_home.get_room_devices(room)
                available = [d['name'] for d in room_devices]
            
            error_msg = f"I couldn't find '{device_type or 'device'}' in '{room or 'any room'}'."
            if available:
                error_msg += f" Available in {room}: {', '.join(available[:3])}"
            
            return {
                'success': False,
                'message': error_msg,
                'command': original_command
            }
        
        # Execute command
        result = virtual_home.control_device(device_id, action)
        result['command'] = original_command
        result['ai_response'] = self._generate_response(result)
        
        return result
    
    def _is_dynamic_command(self, command: str) -> bool:
        """Check if command is dynamic (all, everything, etc.)"""
        dynamic_keywords = [
            'all', 'everything', 'every', 'entire', 'whole',
            'all devices', 'all lights', 'all the', 'every device'
        ]
        return any(kw in command for kw in dynamic_keywords)
    
    def _process_dynamic_command(self, command: str, virtual_home, original_command: str) -> Dict:
        """Process dynamic commands like 'turn off all lights'"""
        # Determine action
        if 'turn on' in command or 'switch on' in command or 'enable' in command or 'start' in command:
            action = 'on'
        elif 'turn off' in command or 'switch off' in command or 'disable' in command or 'stop' in command:
            action = 'off'
        else:
            return {
                'success': False,
                'message': "Please specify 'turn on' or 'turn off'",
                'command': original_command
            }
        
        # Determine scope
        room = None
        device_type = None
        
        # Check for room
        room_keywords = {
            'reception': ['reception', 'living room', 'rec'],
            'bathroom': ['bathroom', 'bath'],
            'kitchen': ['kitchen', 'kit'],
            'room1': ['room 1', 'room1', 'r1', 'bedroom 1'],
            'room2': ['room 2', 'room2', 'r2', 'bedroom 2'],
            'corridors': ['corridor', 'hallway', 'corr'],
            'outdoor': ['outdoor', 'outside', 'out door']
        }
        
        for room_name, keywords in room_keywords.items():
            if any(kw in command for kw in keywords):
                room = room_name
                break
        
        # Check for device type
        if 'light' in command or 'lights' in command:
            device_type = 'light'
        elif 'ac' in command or 'air condition' in command:
            device_type = 'ac'
        elif 'window' in command or 'windows' in command:
            device_type = 'window'
        elif 'sound' in command or 'speaker' in command:
            device_type = 'sound'
        elif 'fan' in command or 'fans' in command:
            device_type = 'fan'
        
        # Get devices to control
        devices_to_control = []
        all_devices = virtual_home.get_all_devices()
        
        for device in all_devices:
            dev_id = device['device_id']
            dev_room = device['room']
            dev_type = device['type']
            
            # Filter by room and/or device type
            if room and device_type:
                # Specific room and type
                if dev_room == room and dev_type == device_type:
                    devices_to_control.append(dev_id)
            elif room:
                # All devices in room
                if dev_room == room:
                    devices_to_control.append(dev_id)
            elif device_type:
                # All devices of type
                if dev_type == device_type:
                    devices_to_control.append(dev_id)
            else:
                # All devices everywhere
                devices_to_control.append(dev_id)
        
        if not devices_to_control:
            return {
                'success': False,
                'message': f"No devices found matching your criteria",
                'command': original_command
            }
        
        # Execute command on all devices
        results = []
        for dev_id in devices_to_control:
            result = virtual_home.control_device(dev_id, action)
            if result['success']:
                results.append(result)
        
        # Generate response
        count = len(results)
        state = 'ON' if action == 'on' else 'OFF'
        
        if room and device_type:
            message = f"Turned {state} {count} {device_type}(s) in {room}"
        elif room:
            message = f"Turned {state} {count} devices in {room}"
        elif device_type:
            message = f"Turned {state} {count} {device_type}(s)"
        else:
            message = f"Turned {state} {count} devices"
        
        return {
            'success': True,
            'message': message,
            'command': original_command,
            'ai_response': message,
            'devices_affected': count,
            'device_ids': devices_to_control
        }
    
    def _generate_response(self, result: Dict) -> str:
        """Generate natural language response"""
        if result['success']:
            device_name = result.get('message', '').split(' turned ')[0]
            state = 'ON' if result['state'] == 1 else 'OFF'
            
            responses = [
                f"Done! I've turned {state.lower()} the {device_name}.",
                f"Sure thing! {device_name} is now {state.lower()}.",
                f"Okay, {device_name} has been turned {state.lower()}.",
                f"All set! The {device_name} is {state.lower()} now."
            ]
            return random.choice(responses)
        else:
            return result.get('message', 'Sorry, something went wrong.')
    
    def get_suggestions(self, env_data: Dict) -> List[str]:
        """Get AI suggestions for user"""
        suggestions = []
        
        if env_data['temperature'] > 28:
            suggestions.append(f"Temperature is {env_data['temperature']}°C. Consider turning on AC.")
        
        if env_data['temperature'] < 20:
            suggestions.append(f"Temperature is {env_data['temperature']}°C. Consider turning on heater.")
        
        if env_data['motion'] == 0:
            suggestions.append("No motion detected. Turn off lights to save energy.")
        
        hour = datetime.now().hour
        if hour >= 22:
            suggestions.append("It's late. Enable night mode to dim lights.")
        
        if env_data.get('light_level', 1000) < 100 and hour < 22:
            suggestions.append("Light level is low. Turn on lights for better visibility.")
        
        return suggestions
    
    def toggle_auto_mode(self) -> Dict:
        """Toggle auto control mode"""
        self.auto_mode = not self.auto_mode
        return {
            'auto_mode': self.auto_mode,
            'message': f"Auto mode {'enabled' if self.auto_mode else 'disabled'}"
        }
    
    def get_auto_mode_status(self) -> bool:
        """Get current auto mode status"""
        return self.auto_mode
    
    def get_statistics(self) -> Dict:
        """Get AI statistics"""
        total_decisions = len(self.decisions_log)
        
        if total_decisions == 0:
            return {
                'total_decisions': 0,
                'most_triggered_rule': None,
                'average_actions_per_decision': 0
            }
        
        # Count rule triggers
        rule_counts = {}
        total_actions = 0
        
        for decision in self.decisions_log:
            total_actions += len(decision['actions'])
            for action in decision['actions']:
                rule_name = action['rule']
                rule_counts[rule_name] = rule_counts.get(rule_name, 0) + 1
        
        most_triggered = max(rule_counts.items(), key=lambda x: x[1]) if rule_counts else (None, 0)
        
        return {
            'total_decisions': total_decisions,
            'most_triggered_rule': most_triggered[0],
            'most_triggered_count': most_triggered[1],
            'average_actions_per_decision': round(total_actions / total_decisions, 2),
            'rule_triggers': rule_counts
        }


# Global instance
ai_engine = AIEngine()
