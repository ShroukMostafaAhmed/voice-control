"""
AI Decision Engine with Machine Learning
Uses trained models to make intelligent decisions
"""

import numpy as np
import joblib
import os
from datetime import datetime
from typing import Dict, List
import json

class MLAIEngine:
    """ML-powered AI Engine for smart home automation"""
    
    def __init__(self, models_dir='models'):
        self.models_dir = models_dir
        self.model = None  # Single model for all devices
        self.scaler = None
        self.metadata = None
        self.auto_mode = False
        self.decisions_log = []
        self.device_columns = []
        
        # Load model
        self._load_model()
    
    def _load_model(self):
        """Load trained single model from disk"""
        if not os.path.exists(self.models_dir):
            print(f"⚠️  Models directory not found: {self.models_dir}")
            print("   Please run 'python data_generator.py' and 'python train_single_model.py' first")
            return False
        
        print(f"📂 Loading AI model from {self.models_dir}/...")
        
        try:
            # Load metadata
            metadata_path = f"{self.models_dir}/metadata.json"
            if os.path.exists(metadata_path):
                with open(metadata_path, 'r') as f:
                    self.metadata = json.load(f)
                    self.device_columns = self.metadata.get('device_columns', [])
                print(f"   ✓ Loaded metadata (trained: {self.metadata.get('trained_at', 'unknown')})")
            
            # Load scaler
            scaler_path = f"{self.models_dir}/scaler.pkl"
            if os.path.exists(scaler_path):
                self.scaler = joblib.load(scaler_path)
                print(f"   ✓ Loaded feature scaler")
            
            # Load single model
            model_path = f"{self.models_dir}/smart_home_model.pkl"
            if os.path.exists(model_path):
                self.model = joblib.load(model_path)
                print(f"   ✓ Loaded smart home model")
                print(f"   ✓ Model predicts {len(self.device_columns)} devices")
            else:
                print(f"   ⚠️  Model not found: {model_path}")
                return False
            
            print(f"\n✅ AI model loaded successfully!")
            return True
        
        except Exception as e:
            print(f"❌ Error loading model: {e}")
            return False
    
    def make_decision(self, env_data: Dict) -> List[Dict]:
        """Make intelligent decisions based on environment data"""
        if not self.model or not self.scaler:
            print("⚠️  Model not loaded, using fallback rules")
            return self._fallback_rules(env_data)
        
        try:
            # Prepare features
            features = self._prepare_features(env_data)
            features_scaled = self.scaler.transform([features])
            
            # Predict ALL device states at once
            predictions = self.model.predict(features_scaled)[0]
            
            # Convert predictions to actions
            actions = []
            for i, device_col in enumerate(self.device_columns):
                device_name = device_col.replace('_status', '')
                prediction = predictions[i]
                
                # Add action
                actions.append({
                    'device_id': device_name,
                    'action': 'on' if prediction == 1 else 'off',
                    'reason': f'ML prediction',
                    'confidence': 0.85,  # Multi-output doesn't provide per-device confidence
                    'scenario': 'ml_based'
                })
            
            # Log decision
            self._log_decision(env_data, 'ml_based', actions)
            
            return actions
        
        except Exception as e:
            print(f"❌ Error in ML decision making: {e}")
            return self._fallback_rules(env_data)
    
    def _prepare_features(self, env_data: Dict) -> List:
        """Prepare features from environment data"""
        now = datetime.now()
        
        features = [
            now.hour,                                    # hour
            now.weekday(),                               # day_of_week
            now.month,                                   # month
            1 if now.weekday() >= 5 else 0,             # is_weekend
            env_data.get('temperature', 25),             # temperature
            env_data.get('humidity', 50),                # humidity
            env_data.get('motion', 0),                   # motion_detected
            env_data.get('light_level', 300),            # light_level
            env_data.get('smoke_detected', 0),           # smoke_detected
            1,                                           # user_present (assume yes)
            env_data.get('temperature', 25) - 2,         # outdoor_temp (estimate)
            0                                            # rain (assume no)
        ]
        
        return features
    
    def _fallback_rules(self, env_data: Dict) -> List[Dict]:
        """Fallback to rule-based system if ML fails"""
        actions = []
        temp = env_data.get('temperature', 25)
        motion = env_data.get('motion', 0)
        smoke = env_data.get('smoke_detected', 0)
        light = env_data.get('light_level', 300)
        hour = datetime.now().hour
        
        # Fire emergency
        if smoke == 1:
            actions.extend([
                {'device_id': 'rec_window', 'action': 'on', 'reason': 'Fire emergency - open windows'},
                {'device_id': 'kit_window', 'action': 'on', 'reason': 'Fire emergency - open windows'},
                {'device_id': 'r1_window', 'action': 'on', 'reason': 'Fire emergency - open windows'}
            ])
        
        # High temperature
        elif temp > 28 and motion == 1:
            actions.extend([
                {'device_id': 'rec_ac', 'action': 'on', 'reason': 'High temperature + motion'},
                {'device_id': 'r1_ac', 'action': 'on', 'reason': 'High temperature + motion'}
            ])
        
        # Low temperature
        elif temp < 20:
            actions.append({'device_id': 'bath_heater', 'action': 'on', 'reason': 'Low temperature'})
        
        # Motion detected
        if motion == 1 and light < 100:
            actions.extend([
                {'device_id': 'corr_main_light', 'action': 'on', 'reason': 'Motion in dark area'},
                {'device_id': 'rec_light', 'action': 'on', 'reason': 'Motion in dark area'}
            ])
        
        # No motion
        elif motion == 0:
            actions.extend([
                {'device_id': 'corr_main_light', 'action': 'off', 'reason': 'No motion detected'},
                {'device_id': 'corr_spots', 'action': 'off', 'reason': 'No motion detected'}
            ])
        
        # Night mode
        if hour >= 22:
            actions.extend([
                {'device_id': 'r1_tv', 'action': 'off', 'reason': 'Night mode'},
                {'device_id': 'rec_sound', 'action': 'off', 'reason': 'Night mode'}
            ])
        
        # Morning routine
        elif hour == 7:
            actions.extend([
                {'device_id': 'bath_light', 'action': 'on', 'reason': 'Morning routine'},
                {'device_id': 'kit_light', 'action': 'on', 'reason': 'Morning routine'}
            ])
        
        return actions
    
    def execute_actions(self, actions: List[Dict], virtual_home) -> List[Dict]:
        """Execute predicted actions on virtual home"""
        results = []
        
        for action in actions:
            device_id = action['device_id']
            command = action['action']
            
            try:
                result = virtual_home.control_device(device_id, command)
                result['reason'] = action.get('reason', 'ML prediction')
                result['confidence'] = action.get('confidence', 0.0)
                result['scenario'] = action.get('scenario', 'unknown')
                results.append(result)
            except Exception as e:
                print(f"   Error executing action on {device_id}: {e}")
        
        return results
    
    def _log_decision(self, env_data: Dict, scenario: str, actions: List[Dict]):
        """Log AI decision for analysis"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'environment': env_data,
            'scenario': scenario,
            'actions': actions,
            'num_actions': len(actions)
        }
        
        self.decisions_log.append(log_entry)
        
        # Keep only last 100 decisions
        if len(self.decisions_log) > 100:
            self.decisions_log = self.decisions_log[-100:]
    
    def get_statistics(self) -> Dict:
        """Get AI decision statistics"""
        if not self.decisions_log:
            return {
                'total_decisions': 0,
                'total_actions': 0,
                'scenarios': {},
                'avg_actions_per_decision': 0
            }
        
        scenarios = {}
        total_actions = 0
        
        for log in self.decisions_log:
            scenario = log.get('scenario', 'unknown')
            scenarios[scenario] = scenarios.get(scenario, 0) + 1
            total_actions += log.get('num_actions', 0)
        
        return {
            'total_decisions': len(self.decisions_log),
            'total_actions': total_actions,
            'scenarios': scenarios,
            'avg_actions_per_decision': total_actions / len(self.decisions_log) if self.decisions_log else 0,
            'models_loaded': 1 if self.model else 0,
            'ml_enabled': bool(self.model)
        }
    
    def set_auto_mode(self, enabled: bool):
        """Enable/disable auto mode"""
        self.auto_mode = enabled
        return self.auto_mode
    
    def get_auto_mode_status(self) -> bool:
        """Get auto mode status"""
        return self.auto_mode


# Global instance
ml_ai_engine = MLAIEngine()
