# Smart Home Database

SQLite database for Smart Home Control System with AI integration support.

## Database Structure

### Tables

1. **devices** - All smart home devices
   - device_id, name, room, type, status, last_updated

2. **sensors_log** - Sensor readings history
   - sensor_type, value, room, timestamp

3. **device_events** - Device state changes log
   - device_id, event_type, old_status, new_status, triggered_by, timestamp

4. **user_commands** - Voice/text commands history
   - command_text, interpreted_intent, executed_action, success, timestamp

5. **ai_learning_data** - Training data for AI models
   - hour, day_of_week, temperature, humidity, motion_detected, user_present, device_id, device_status, timestamp

6. **automation_rules** - Automation rules
   - rule_name, condition, action, priority, enabled

7. **energy_usage** - Energy consumption tracking
   - device_id, power_watts, duration_minutes, total_kwh, cost, timestamp

8. **alerts** - System alerts
   - alert_type, severity, message, room, resolved, timestamp

## Setup

### 1. Initialize Database

```bash
cd database
python init_db.py
```

This will create `smart_home.db` with schema and seed data.

### 2. Use Database Helper

```python
from db_helper import SmartHomeDB

db = SmartHomeDB()

# Get all devices
devices = db.get_all_devices()

# Update device status
db.update_device_status('rec_light', 1, triggered_by='user')

# Log sensor data
db.log_sensor_data('temperature', 25.5, 'reception')

# Get AI training data
training_data = db.get_ai_training_data(days=30)

# Export for AI model
db.export_training_data_json('training_data.json')
```

## AI Integration

### Training Data Format

The `ai_learning_data` table contains:
- **Features**: hour, day_of_week, temperature, humidity, motion_detected, user_present
- **Target**: device_status (0 or 1)

### Example: Get Training Data for ML Model

```python
import pandas as pd
from db_helper import SmartHomeDB

db = SmartHomeDB()
data = db.get_ai_training_data(days=90)

# Convert to DataFrame
df = pd.DataFrame(data)

# Features
X = df[['hour', 'day_of_week', 'temperature', 'humidity', 'motion_detected', 'user_present']]

# Target
y = df['device_status']

# Train your model
from sklearn.ensemble import RandomForestClassifier
model = RandomForestClassifier()
model.fit(X, y)
```

### Example: Predict Device State

```python
# Get current state
state = db.get_current_state_for_ai()

# Predict if light should be on
features = [
    state['hour'],
    state['day_of_week'],
    state['temperature'],
    state['humidity'],
    state['motion_detected'],
    1  # user_present
]

prediction = model.predict([features])
print(f"Light should be: {'ON' if prediction[0] == 1 else 'OFF'}")
```

## API Examples

### Device Operations

```python
# Get device by ID
device = db.get_device_by_id('rec_light')

# Get devices by room
room_devices = db.get_devices_by_room('reception')

# Update device status
db.update_device_status('rec_ac', 1, triggered_by='ai')
```

### Sensor Operations

```python
# Log sensor reading
db.log_sensor_data('temperature', 26.5, 'reception')

# Get latest reading
latest = db.get_latest_sensor_data('temperature', room='reception')

# Get history
history = db.get_sensor_history('temperature', hours=24)
```

### Energy Tracking

```python
# Log energy usage
db.log_energy_usage('r1_ac', power_watts=1500, duration_minutes=120)

# Get energy report
report = db.get_energy_report(days=7)
print(f"Total: {report['total_kwh']} kWh, Cost: ${report['total_cost']}")
```

### Automation Rules

```python
# Get active rules
rules = db.get_active_rules()

# Add new rule
db.add_automation_rule(
    rule_name='Evening Lights',
    condition='time = 18:00 AND user_present = 1',
    action='turn_on_reception_light',
    priority=2
)
```

### Alerts

```python
# Create alert
db.create_alert('high_temperature', 'warning', 'Temperature exceeded 30°C', room='reception')

# Get unresolved alerts
alerts = db.get_unresolved_alerts()
```

## Data Export for AI

```python
# Export training data as JSON
db.export_training_data_json('training_data.json')

# Get device usage patterns
pattern = db.get_device_usage_pattern('rec_light')
# Returns: hour, day_of_week, avg_status, count

# Get device statistics
stats = db.get_device_statistics()
```

## Database File

- **Location**: `database/smart_home.db`
- **Type**: SQLite3
- **Size**: ~100KB with seed data
- **Portable**: Single file, easy to backup

## Notes

- All timestamps are in UTC
- Device status: 0 = OFF, 1 = ON
- Day of week: 0 = Monday, 6 = Sunday
- Energy cost calculated at $0.15 per kWh (default)
