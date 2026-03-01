"""
Advanced AI Engine - Professional Integration
Combines: ML Models + Rule-Based + Mistral AI
"""

from ai_engine import ai_engine as rule_engine
from ai_engine_ml import ml_ai_engine
from mistral_client import mistral_client
from typing import Dict, List
from datetime import datetime
import json

class AdvancedAIEngine:
    """
    Professional AI Engine with multiple layers:
    1. ML Models for predictions
    2. Rule-Based for safety/emergencies
    3. Mistral AI for natural language
    """
    
    def __init__(self):
        self.ml_engine = ml_ai_engine
        self.rule_engine = rule_engine
        self.mistral = mistral_client
        self.auto_mode = False
        self.decisions_log = []
        
        # Configuration
        self.use_ml = True
        self.use_mistral = True
        self.emergency_use_rules = True  # Always use rules for emergencies
        
        print("\n" + "="*70)
        print("🤖 Advanced AI Engine Initialized")
        print("="*70)
        print(f"   ML Model: {'✓ Loaded' if self.ml_engine.model else '✗ Not loaded'}")
        print(f"   Rule Engine: ✓ Ready")
        print(f"   Mistral AI: {'✓ Available' if self.mistral.is_available() else '✗ Not available'}")
        print("="*70 + "\n")
    
    def parse_command(self, command: str, env_data: Dict) -> Dict:
        """
        Parse natural language command
        Priority: Mistral AI > Fallback Parser
        """
        print(f"\n[COMMAND] '{command}'")
        
        # Try Mistral first if available
        if self.use_mistral and self.mistral.is_available():
            print("[PARSER] Using Mistral AI...")
            try:
                result = self.mistral.parse_command(command, env_data)
                if result.get('action') != 'fallback':
                    print(f"[MISTRAL] ✓ Parsed: {result.get('device_id')} -> {result.get('command')}")
                    return result
            except Exception as e:
                print(f"[MISTRAL] ✗ Error: {e}")
        
        # Fallback to simple parser
        print("[PARSER] Using fallback parser...")
        return self._fallback_parser(command)
    
    def _fallback_parser(self, command: str) -> Dict:
        """Simple fallback parser"""
        command = command.lower()
        
        # Extract action
        if 'turn on' in command or 'open' in command or 'enable' in command:
            action = 'on'
        elif 'turn off' in command or 'close' in command or 'disable' in command:
            action = 'off'
        else:
            return {'action': 'unknown', 'device_id': None, 'command': None}
        
        # Extract device
        device_map = {
            'reception light': 'rec_light',
            'reception ac': 'rec_ac',
            'reception window': 'rec_window',
            'reception sound': 'rec_sound',
            'kitchen light': 'kit_light',
            'kitchen fan': 'kit_fan',
            'kitchen window': 'kit_window',
            'bathroom light': 'bath_light',
            'bathroom heater': 'bath_heater',
            'bathroom fan': 'bath_fan',
            'room 1 light': 'r1_light',
            'room 1 ac': 'r1_ac',
            'room 1 tv': 'r1_tv',
            'room 1 window': 'r1_window',
            'room 2 light': 'r2_light',
            'room 2 ac': 'r2_ac',
            'corridor light': 'corr_main_light',
            'outdoor light': 'out_light',
            'outdoor door': 'out_door',
        }
        
        for key, device_id in device_map.items():
            if key in command:
                return {
                    'action': 'control_device',
                    'device_id': device_id,
                    'command': action,
                    'explanation': 'Fallback parser',
                    'confidence': 0.7
                }
        
        return {'action': 'unknown', 'device_id': None, 'command': None}
    
    def make_decision(self, env_data: Dict) -> List[Dict]:
        """
        Make intelligent decision using multi-layer approach
        """
        scenario_type = self._classify_situation(env_data)
        
        print(f"\n[DECISION] Situation: {scenario_type}")
        
        # Layer 1: Emergency - Always use rules (fastest, safest)
        if scenario_type == 'emergency':
            print("[ENGINE] Using Rule-Based (Emergency)")
            actions = self.rule_engine.make_decision(env_data)
            self._add_metadata(actions, 'rule-based', 'emergency')
            return actions
        
        # Layer 2: Normal - Use ML if available
        if scenario_type == 'normal' and self.use_ml and self.ml_engine.model:
            print("[ENGINE] Using ML Model")
            actions = self.ml_engine.make_decision(env_data)
            
            # Filter low confidence predictions
            filtered_actions = [
                a for a in actions 
                if a.get('confidence', 0) > 0.6
            ]
            
            if filtered_actions:
                self._add_metadata(filtered_actions, 'ml-based', 'normal')
                print(f"[ML] ✓ {len(filtered_actions)} high-confidence actions")
                return filtered_actions
            else:
                print("[ML] ⚠️  Low confidence, falling back to rules")
        
        # Layer 3: Fallback - Use rules
        print("[ENGINE] Using Rule-Based (Fallback)")
        actions = self.rule_engine.make_decision(env_data)
        self._add_metadata(actions, 'rule-based', 'fallback')
        return actions
    
    def _classify_situation(self, env_data: Dict) -> str:
        """Classify situation as emergency or normal"""
        # Emergency conditions
        if env_data.get('smoke_detected', 0) == 1:
            return 'emergency'
        
        if env_data.get('temperature', 25) > 40:
            return 'emergency'
        
        # Add more emergency conditions here
        
        return 'normal'
    
    def _add_metadata(self, actions: List[Dict], engine: str, reason: str):
        """Add metadata to actions"""
        for action in actions:
            action['engine'] = engine
            action['reason_type'] = reason
    
    def execute_actions(self, actions: List[Dict], virtual_home) -> List[Dict]:
        """Execute actions with logging"""
        results = []
        
        print(f"\n[EXECUTE] Running {len(actions)} actions...")
        
        for i, action in enumerate(actions, 1):
            device_id = action.get('device_id')
            command = action.get('action')
            
            if not device_id or not command:
                continue
            
            try:
                result = virtual_home.control_device(device_id, command)
                result['reason'] = action.get('reason', 'Unknown')
                result['confidence'] = action.get('confidence', 0.0)
                result['scenario'] = action.get('scenario', 'unknown')
                result['engine'] = action.get('engine', 'unknown')
                
                status = '✓' if result.get('success') else '✗'
                print(f"   [{i}/{len(actions)}] {status} {device_id}: {command.upper()}")
                
                results.append(result)
            except Exception as e:
                print(f"   [{i}/{len(actions)}] ✗ Error on {device_id}: {e}")
        
        # Log decision
        self._log_decision(actions, results)
        
        return results
    
    def _log_decision(self, actions: List[Dict], results: List[Dict]):
        """Log decision for analysis"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'actions': len(actions),
            'successful': sum(1 for r in results if r.get('success')),
            'failed': sum(1 for r in results if not r.get('success')),
            'engines_used': list(set(a.get('engine', 'unknown') for a in actions))
        }
        
        self.decisions_log.append(log_entry)
        
        # Keep only last 100
        if len(self.decisions_log) > 100:
            self.decisions_log = self.decisions_log[-100:]
    
    def generate_response(self, result: Dict, original_command: str) -> str:
        """Generate natural language response"""
        # Try Mistral first
        if self.use_mistral and self.mistral.is_available():
            try:
                response = self.mistral.generate_response(result, original_command)
                if response and len(response) < 100:
                    return response
            except Exception as e:
                print(f"[MISTRAL] Response generation error: {e}")
        
        # Fallback response
        if result.get('success'):
            return result.get('message', 'Done successfully')
        else:
            return result.get('message', 'Failed to execute')
    
    def get_statistics(self) -> Dict:
        """Get comprehensive statistics"""
        ml_stats = self.ml_engine.get_statistics()
        
        # Add advanced stats
        if self.decisions_log:
            total_actions = sum(log['actions'] for log in self.decisions_log)
            total_successful = sum(log['successful'] for log in self.decisions_log)
            
            engines_count = {}
            for log in self.decisions_log:
                for engine in log['engines_used']:
                    engines_count[engine] = engines_count.get(engine, 0) + 1
        else:
            total_actions = 0
            total_successful = 0
            engines_count = {}
        
        return {
            'total_decisions': len(self.decisions_log),
            'total_actions': total_actions,
            'total_successful': total_successful,
            'success_rate': (total_successful / total_actions * 100) if total_actions > 0 else 0,
            'engines_used': engines_count,
            'ml_enabled': bool(self.ml_engine.model),
            'ml_model_loaded': 1 if self.ml_engine.model else 0,
            'mistral_available': self.mistral.is_available(),
            'auto_mode': self.auto_mode,
            **ml_stats
        }
    
    def get_suggestions(self, env_data: Dict) -> List[str]:
        """Get AI suggestions"""
        # Use rule engine for suggestions
        return self.rule_engine.get_suggestions(env_data)
        """Enable/disable auto mode"""
        self.auto_mode = enabled
        self.ml_engine.set_auto_mode(enabled)
        self.rule_engine.auto_mode = enabled
        
        print(f"\n[AUTO MODE] {'Enabled ✓' if enabled else 'Disabled ✗'}")
        
        return self.auto_mode
    
    def get_auto_mode_status(self) -> bool:
        """Get auto mode status"""
        return self.auto_mode
    
    def get_system_info(self) -> Dict:
        """Get system information"""
        return {
            'version': '2.0-Advanced',
            'components': {
                'ml_model': {
                    'status': 'loaded' if self.ml_engine.model else 'not_loaded',
                    'devices': len(self.ml_engine.device_columns) if self.ml_engine.model else 0,
                    'accuracy': '85-95%'
                },
                'rule_engine': {
                    'status': 'ready',
                    'rules': 8
                },
                'mistral_ai': {
                    'status': 'available' if self.mistral.is_available() else 'not_available',
                    'model': self.mistral.model_name
                }
            },
            'features': [
                'ML-based predictions (single model)',
                'Rule-based safety',
                'Natural language (Mistral)',
                'Multi-layer decision making',
                'Confidence scoring',
                'Scenario detection',
                'Auto mode'
            ]
        }


# Global instance
advanced_ai_engine = AdvancedAIEngine()
