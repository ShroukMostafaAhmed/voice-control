"""
Compare Rule-Based AI vs ML-Based AI
Shows the difference in decision making
"""

from ai_engine import ai_engine as rule_based_engine
from ai_engine_ml import ml_ai_engine
from virtual_devices import virtual_home
import time

def print_separator():
    print("\n" + "=" * 80 + "\n")

def compare_scenario(name, env_data):
    """Compare both systems on the same scenario"""
    print(f"📊 Scenario: {name}")
    print(f"   Environment: Temp={env_data.get('temperature')}°C, "
          f"Motion={env_data.get('motion')}, "
          f"Light={env_data.get('light_level')} lux, "
          f"Smoke={env_data.get('smoke_detected')}")
    
    print("\n   🔧 Rule-Based AI:")
    rule_actions = rule_based_engine.make_decision(env_data)
    if not rule_actions:
        print("      No actions")
    else:
        for action in rule_actions[:5]:  # Show first 5
            print(f"      • {action['device_id']}: {action['action'].upper()}")
    print(f"      Total actions: {len(rule_actions)}")
    
    print("\n   🤖 ML-Based AI:")
    if ml_ai_engine.model:
        ml_actions = ml_ai_engine.make_decision(env_data)
        if not ml_actions:
            print("      No actions")
        else:
            for action in ml_actions[:5]:  # Show first 5
                confidence = action.get('confidence', 0)
                print(f"      • {action['device_id']}: {action['action'].upper()} "
                      f"(confidence: {confidence:.1%})")
        print(f"      Total actions: {len(ml_actions)}")
        
        # Show scenario detection
        if ml_actions and 'scenario' in ml_actions[0]:
            print(f"      Detected scenario: {ml_actions[0]['scenario']}")
    else:
        print("      ⚠️  ML model not loaded")
    
    print_separator()
    time.sleep(0.5)

def main():
    print("=" * 80)
    print("AI Systems Comparison: Rule-Based vs Machine Learning")
    print("=" * 80)
    
    if not ml_ai_engine.model:
        print("\n⚠️  WARNING: ML model not loaded!")
        print("   The comparison will show rule-based system only.")
        print("   To train ML model, run:")
        print("   1. python data_generator.py")
        print("   2. python train_single_model.py")
        print_separator()
    
    # Test scenarios
    
    compare_scenario("🔥 Fire Emergency", {
        'temperature': 35,
        'humidity': 50,
        'motion': 1,
        'light_level': 300,
        'smoke_detected': 1,
        'hour': 14
    })
    
    compare_scenario("🌡️ Extreme Heat", {
        'temperature': 36,
        'humidity': 45,
        'motion': 1,
        'light_level': 700,
        'smoke_detected': 0,
        'hour': 15
    })
    
    compare_scenario("☀️ Hot Day", {
        'temperature': 30,
        'humidity': 45,
        'motion': 1,
        'light_level': 600,
        'smoke_detected': 0,
        'hour': 14
    })
    
    compare_scenario("❄️ Cold Morning", {
        'temperature': 18,
        'humidity': 55,
        'motion': 1,
        'light_level': 200,
        'smoke_detected': 0,
        'hour': 7
    })
    
    compare_scenario("🌙 Late Night", {
        'temperature': 24,
        'humidity': 50,
        'motion': 1,
        'light_level': 50,
        'smoke_detected': 0,
        'hour': 23
    })
    
    compare_scenario("💡 Dark Room", {
        'temperature': 25,
        'humidity': 50,
        'motion': 1,
        'light_level': 80,
        'smoke_detected': 0,
        'hour': 20
    })
    
    compare_scenario("💤 No Activity", {
        'temperature': 25,
        'humidity': 50,
        'motion': 0,
        'light_level': 300,
        'smoke_detected': 0,
        'hour': 16
    })
    
    # Summary
    print("📈 Summary:")
    print("\n   Rule-Based AI:")
    print("      ✓ Fast and predictable")
    print("      ✓ Easy to understand")
    print("      ✓ No training needed")
    print("      ✗ Limited to predefined rules")
    print("      ✗ Cannot learn from data")
    print("      ✗ May miss complex patterns")
    
    print("\n   ML-Based AI:")
    print("      ✓ Learns from data")
    print("      ✓ Adapts to patterns")
    print("      ✓ Handles complex scenarios")
    print("      ✓ Provides confidence scores")
    print("      ✓ Can detect scenarios automatically")
    print("      ✗ Requires training data")
    print("      ✗ Needs periodic retraining")
    print("      ✗ Less predictable")
    
    print("\n   💡 Recommendation:")
    print("      Use ML-Based AI for:")
    print("      - Complex decision making")
    print("      - Learning user patterns")
    print("      - Adaptive automation")
    print("      - Scenario detection")
    
    print("\n      Use Rule-Based AI for:")
    print("      - Simple, predictable rules")
    print("      - Safety-critical decisions")
    print("      - Fallback when ML fails")
    print("      - Quick prototyping")
    
    print_separator()
    print("✅ Comparison complete!")

if __name__ == "__main__":
    main()
