"""
Simple Example: Using ML-Based AI Engine
"""

from ai_engine_ml import ml_ai_engine
from virtual_devices import virtual_home

def example_1_fire_emergency():
    """Example 1: Fire Emergency Response"""
    print("=" * 60)
    print("Example 1: Fire Emergency 🔥")
    print("=" * 60)
    
    # Simulate fire emergency
    env_data = {
        'temperature': 35,
        'humidity': 50,
        'motion': 1,
        'light_level': 300,
        'smoke_detected': 1,  # FIRE!
    }
    
    print("\n📊 Environment:")
    print(f"   Temperature: {env_data['temperature']}°C")
    print(f"   Smoke Detected: {'YES ⚠️' if env_data['smoke_detected'] else 'No'}")
    
    # AI makes decision
    print("\n🤖 AI is analyzing...")
    actions = ml_ai_engine.make_decision(env_data)
    
    print(f"\n✅ AI Decision: {len(actions)} actions")
    for action in actions:
        print(f"   • {action['device_id']}: {action['action'].upper()}")
        print(f"     Reason: {action.get('reason', 'N/A')}")
        if 'confidence' in action:
            print(f"     Confidence: {action['confidence']:.1%}")
    
    # Execute actions
    print("\n⚙️  Executing actions...")
    results = ml_ai_engine.execute_actions(actions, virtual_home)
    
    print(f"\n✓ Executed {len(results)} actions successfully")
    print("\n" + "=" * 60 + "\n")

def example_2_hot_day():
    """Example 2: Hot Day - Turn on AC"""
    print("=" * 60)
    print("Example 2: Hot Day ☀️")
    print("=" * 60)
    
    env_data = {
        'temperature': 32,
        'humidity': 45,
        'motion': 1,
        'light_level': 600,
        'smoke_detected': 0,
    }
    
    print("\n📊 Environment:")
    print(f"   Temperature: {env_data['temperature']}°C (Hot!)")
    print(f"   Motion: {'Detected' if env_data['motion'] else 'None'}")
    
    print("\n🤖 AI is analyzing...")
    actions = ml_ai_engine.make_decision(env_data)
    
    print(f"\n✅ AI Decision: {len(actions)} actions")
    for action in actions[:5]:  # Show first 5
        print(f"   • {action['device_id']}: {action['action'].upper()}")
        if 'confidence' in action:
            print(f"     Confidence: {action['confidence']:.1%}")
    
    results = ml_ai_engine.execute_actions(actions, virtual_home)
    print(f"\n✓ Executed {len(results)} actions")
    print("\n" + "=" * 60 + "\n")

def example_3_night_mode():
    """Example 3: Night Mode - Dim lights"""
    print("=" * 60)
    print("Example 3: Night Mode 🌙")
    print("=" * 60)
    
    env_data = {
        'temperature': 24,
        'humidity': 50,
        'motion': 1,
        'light_level': 50,
        'smoke_detected': 0,
    }
    
    print("\n📊 Environment:")
    print(f"   Time: Late night")
    print(f"   Light Level: {env_data['light_level']} lux (Dark)")
    
    print("\n🤖 AI is analyzing...")
    actions = ml_ai_engine.make_decision(env_data)
    
    print(f"\n✅ AI Decision: {len(actions)} actions")
    for action in actions[:5]:
        print(f"   • {action['device_id']}: {action['action'].upper()}")
    
    results = ml_ai_engine.execute_actions(actions, virtual_home)
    print(f"\n✓ Executed {len(results)} actions")
    print("\n" + "=" * 60 + "\n")

def example_4_custom_scenario():
    """Example 4: Custom Scenario"""
    print("=" * 60)
    print("Example 4: Custom Scenario 🎯")
    print("=" * 60)
    
    # You can customize this!
    env_data = {
        'temperature': 28,      # Warm
        'humidity': 60,         # Moderate
        'motion': 1,            # Motion detected
        'light_level': 200,     # Dim
        'smoke_detected': 0,    # No smoke
    }
    
    print("\n📊 Your Custom Environment:")
    for key, value in env_data.items():
        print(f"   {key}: {value}")
    
    print("\n🤖 AI is analyzing...")
    actions = ml_ai_engine.make_decision(env_data)
    
    if actions:
        print(f"\n✅ AI Decision: {len(actions)} actions")
        for action in actions:
            print(f"   • {action['device_id']}: {action['action'].upper()}")
            if 'scenario' in action:
                print(f"     Scenario: {action['scenario']}")
        
        results = ml_ai_engine.execute_actions(actions, virtual_home)
        print(f"\n✓ Executed {len(results)} actions")
    else:
        print("\n✅ No actions needed - everything is optimal!")
    
    print("\n" + "=" * 60 + "\n")

def show_statistics():
    """Show AI statistics"""
    print("=" * 60)
    print("AI Statistics 📊")
    print("=" * 60)
    
    stats = ml_ai_engine.get_statistics()
    
    print(f"\n   Total decisions made: {stats['total_decisions']}")
    print(f"   Total actions executed: {stats['total_actions']}")
    print(f"   Average actions per decision: {stats['avg_actions_per_decision']:.2f}")
    print(f"   ML models loaded: {stats['models_loaded']}")
    print(f"   ML enabled: {'Yes ✓' if stats['ml_enabled'] else 'No ✗'}")
    
    if stats['scenarios']:
        print(f"\n   Scenarios detected:")
        for scenario, count in stats['scenarios'].items():
            print(f"      {scenario}: {count} times")
    
    print("\n" + "=" * 60 + "\n")

def main():
    print("\n" + "=" * 60)
    print("Smart Home ML AI - Usage Examples")
    print("=" * 60)
    print()
    
    # Check if model is loaded
    if not ml_ai_engine.model:
        print("❌ ERROR: ML model not loaded!")
        print("\n   Please run the following commands first:")
        print("   1. python data_generator.py")
        print("   2. python train_single_model.py")
        print("\n   Or simply run: QUICK_START_SINGLE.bat")
        return
    
    print(f"✅ ML model loaded: predicts {len(ml_ai_engine.device_columns)} devices")
    print()
    
    # Run examples
    example_1_fire_emergency()
    input("Press Enter to continue...")
    
    example_2_hot_day()
    input("Press Enter to continue...")
    
    example_3_night_mode()
    input("Press Enter to continue...")
    
    example_4_custom_scenario()
    input("Press Enter to continue...")
    
    show_statistics()
    
    print("✅ Examples complete!")
    print("\nYou can now:")
    print("   1. Modify example_4_custom_scenario() with your own data")
    print("   2. Integrate ml_ai_engine into your application")
    print("   3. Run 'python test_ml_model.py' for more tests")
    print("   4. The system uses ONE model instead of 23 models!")

if __name__ == "__main__":
    main()
