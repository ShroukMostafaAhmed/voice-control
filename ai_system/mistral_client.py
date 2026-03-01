"""
Mistral AI Client
Local Mistral model integration via Ollama
"""

import subprocess
import json
import re
from typing import Dict, Optional, List

class MistralClient:
    """Client for local AI model via Ollama"""
    
    def __init__(self, model_name: str = "tinyllama"):
        self.model_name = model_name
        self._available = None
    
    def is_available(self) -> bool:
        """Check if Mistral is available via Ollama"""
        if self._available is not None:
            return self._available
        
        try:
            result = subprocess.run(
                ["ollama", "list"],
                capture_output=True,
                text=True,
                timeout=5
            )
            self._available = self.model_name in result.stdout.lower()
            if self._available:
                print(f"[AI MODEL] '{self.model_name}' is available")
            else:
                print(f"[AI MODEL] '{self.model_name}' not found. Install with: ollama pull {self.model_name}")
            return self._available
        except FileNotFoundError:
            print("[AI MODEL] Ollama not installed. Install from: https://ollama.ai")
            self._available = False
            return False
        except Exception as e:
            print(f"[AI MODEL] Error checking availability: {e}")
            self._available = False
            return False
    
    def parse_command(self, command: str, env_data: Dict) -> Dict:
        """Parse user command using AI model"""
        if not self.is_available():
            return {
                'action': 'fallback',
                'device_id': None,
                'command': None,
                'explanation': 'AI model not available, using fallback',
                'confidence': 0
            }
        
        try:
            # Build prompt
            prompt = self._build_parse_prompt(command, env_data)
            
            # Call AI model with short timeout
            response = self._call_mistral(prompt, timeout=5)
            
            # Parse JSON response
            parsed = self._extract_json(response)
            
            if parsed and parsed.get('device_id'):
                # Convert to expected format
                return {
                    'action': 'control_device',
                    'device_id': parsed.get('device_id'),
                    'command': parsed.get('command'),
                    'explanation': 'Parsed by AI',
                    'confidence': 0.9
                }
            else:
                return {
                    'action': 'fallback',
                    'device_id': None,
                    'command': None,
                    'explanation': 'Using fallback parser',
                    'confidence': 0
                }
        
        except Exception as e:
            print(f"[AI MODEL ERROR] {e} - Using fallback parser")
            return {
                'action': 'fallback',
                'device_id': None,
                'command': None,
                'explanation': 'Using fallback parser',
                'confidence': 0
            }
    
    def generate_response(self, result: Dict, original_command: str) -> str:
        """Generate natural language response"""
        if not self.is_available():
            return result.get('message', 'Done')
        
        try:
            prompt = f"""Generate a short response (max 10 words):

User: "{original_command}"
Action: {result.get('message', 'Unknown')}

Response:"""
            
            response = self._call_mistral(prompt, timeout=5)
            # Clean response
            response = response.strip().strip('"').strip("'")
            return response if len(response) < 100 else result.get('message', 'Done')
        
        except Exception as e:
            print(f"[AI ERROR] {e} - Using default response")
            return result.get('message', 'Done')
    
    def _build_parse_prompt(self, command: str, env_data: Dict) -> str:
        """Build prompt for command parsing"""
        prompt = f"""Parse command to JSON.

Command: "{command}"

Devices (use exact IDs):
bath_light, bath_fire, bath_heater, bath_fan
corr_main_light, corr_spots, corr_fire
rec_light, rec_window, rec_fire, rec_sound, rec_ac
out_camera, out_light, out_door
r1_ac, r1_tv, r1_light, r1_window, r1_fire, r1_sound
kit_light, kit_window, kit_fan, kit_fire
r2_ac, r2_sound, r2_light, r2_fire

Room mappings:
- "room 1" or "room1" or "bedroom 1" → use "r1_"
- "room 2" or "room2" or "bedroom 2" → use "r2_"
- "reception" → use "rec_"
- "bathroom" → use "bath_"
- "kitchen" → use "kit_"
- "outdoor" or "out door" → use "out_"
- "corridor" → use "corr_"

Examples:
"Turn on room 1 light" -> {{"device_id":"r1_light","command":"on"}}
"Turn off room 2 AC" -> {{"device_id":"r2_ac","command":"off"}}
"Turn on bedroom 1 TV" -> {{"device_id":"r1_tv","command":"on"}}
"Open room 1 window" -> {{"device_id":"r1_window","command":"on"}}

JSON only:
{{"device_id":"exact_id","command":"on or off"}}

JSON:"""
        return prompt
    
    def _call_mistral(self, prompt: str, timeout: int = 5) -> str:
        """Call AI model via Ollama"""
        try:
            result = subprocess.run(
                ["ollama", "run", self.model_name, prompt],
                capture_output=True,
                text=True,
                timeout=timeout
            )
            
            if result.returncode == 0:
                return result.stdout.strip()
            else:
                raise Exception(f"Ollama error: {result.stderr}")
        
        except subprocess.TimeoutExpired:
            raise Exception("AI model timeout - try a lighter model")
        except Exception as e:
            raise Exception(f"AI call failed: {e}")
    
    def _extract_json(self, text: str) -> Optional[Dict]:
        """Extract JSON from text"""
        try:
            # Try direct JSON parse
            return json.loads(text)
        except:
            pass
        
        try:
            # Find JSON in text
            start = text.find('{')
            end = text.rfind('}') + 1
            
            if start >= 0 and end > start:
                json_str = text[start:end]
                return json.loads(json_str)
        except:
            pass
        
        return None


# Global instance
mistral_client = MistralClient()

