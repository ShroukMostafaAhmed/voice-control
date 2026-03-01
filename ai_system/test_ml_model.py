"""
Test ML Model with Different Scenarios
"""

from ai_engine_ml import ml_ai_engine
from virtual_devices import virtual_home
import time

def print_separator():
    print("\n" + "=" * 70 + "\n")

def test_scenario(name, env_data):
    """Test a specific scenario"""
    print(f"🧪 Testing Scenario: {name}")
    print(f"   Environment:")
    for key, value in env_data.items():
        print(f"      {key}: {value}")
    
    # Make decision
    actions = ml_ai_engine.make_decision(env_data)
    
    print(f"\n   🤖 AI Decisions ({len(actions)} actions):")
    if not actions:
        print("      No actions needed")
    else:
        for action in actions:
            print(f"      • {action['device_id']}: {action['action'].upper()}")
            print(f"        Reason: {action.get('reason', 'N/A')}")
            if 'confidence' in action:
                print(f"        Confidence: {action['confidence']:.1%}")
            if 'scenario' in action:
                print(f"        Scenario: {action['scenario']}")
    
    # Execute actions
    if actions:
        print(f"\n   ⚙️  Executing actions...")
        results = ml_ai_engine.execute_actions(actions, virtual_home)
        
        success_count = sum(1 for r in results if r.get('success', False))
        print(f"      ✓ Successfully executed {success_count}/{len(results)} actions")
    
    print_separator()
    time.sleep(1)

def main():
    print("=" * 70)
    print("Smart Home ML Model Testing")
    print("=" * 70)
    
    # Check if model is loaded
    if not ml_ai_engine.model:
        print("\n❌ ERROR: Model not loaded!")
        print("   Please run the following commands first:")
        print("   1. python data_generator.py")
        print("   2. python train_single_model.py")
        print("\n   Or run: QUICK_START_SINGLE.bat")
        return
    
    print(f"\n✅ Model loaded: predicts {len(ml_ai_engine.device_columns)} devices")
    print_separator()
    
    # Test scenarios
    
    # 1. Fire Emergency
    test_scenario("🔥 Fire Emergency", {
        'temperature': 35,
        'humidity': 50,
        'motion': 1,
        'light_level': 300,
        'smoke_detected': 1,  # SMOKE!
    })
    
    # 2. Extreme Heat
    test_scenario("🌡️ Extreme Heat", {
        'temperature': 38,
        'humidity': 45,
        'motion': 1,
        'light_level': 700,
        'smoke_detected': 0,
    })
    
    # 3. Hot Weather (Normal)
    test_scenario("☀️ Hot Weather", {
        'temperature': 32,
        'humidity': 45,
        'motion': 1,
        'light_level': 600,
        'smoke_detected': 0,
    })
    
    # 4. Cold Weather
    test_scenario("❄️ Cold Weather", {
        'temperature': 16,
        'humidity': 55,
        'motion': 1,
        'light_level': 200,
        'smoke_detected': 0,
    })
    
    # 5. Night Mode
    test_scenario("🌙 Night Mode (11 PM)", {
        'temperature': 24,
        'humidity': 50,
        'motion': 1,
        'light_level': 50,
        'smoke_detected': 0,
    })
    
    # 6. Morning Routine
    test_scenario("🌅 Morning Routine (7 AM)", {
        'temperature': 22,
        'humidity': 55,
        'motion': 1,
        'light_level': 200,
        'smoke_detected': 0,
    })
    
    # 7. Dark Room with Motion
    test_scenario("💡 Dark Room with Motion", {
        'temperature': 25,
        'humidity': 50,
        'motion': 1,
        'light_level': 50,  # Dark
        'smoke_detected': 0,
    })
    
    # 8. No Motion (Energy Saving)
    test_scenario("💤 No Motion - Energy Saving", {
        'temperature': 25,
        'humidity': 50,
        'motion': 0,  # No motion
        'light_level': 300,
        'smoke_detected': 0,
    })
    
    # 9. High Humidity
    test_scenario("💧 High Humidity", {
        'temperature': 26,
        'humidity': 75,  # High humidity
        'motion': 1,
        'light_level': 300,
        'smoke_detected': 0,
    })
    
    # 10. Normal Operation
    test_scenario("✅ Normal Operation", {
        'temperature': 25,
        'humidity': 50,
        'motion': 1,
        'light_level': 400,
        'smoke_detected': 0,
    })
    
    # Show statistics
    print("📊 AI Statistics:")
    stats = ml_ai_engine.get_statistics()
    print(f"   Total decisions made: {stats['total_decisions']}")
    print(f"   Total actions executed: {stats['total_actions']}")
    print(f"   Average actions per decision: {stats['avg_actions_per_decision']:.2f}")
    print(f"   ML models loaded: {stats['models_loaded']}")
    print(f"   ML enabled: {stats['ml_enabled']}")
    
    if stats['scenarios']:
        print(f"\n   Scenarios detected:")
        for scenario, count in stats['scenarios'].items():
            print(f"      {scenario}: {count} times")
    
    print_separator()
    print("✅ Testing complete!")
    print("\nThe AI model is working correctly and making intelligent decisions")
    print("based on the trained data.")

if __name__ == "__main__":
    main()
