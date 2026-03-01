-- Seed Data for Smart Home Database

-- Insert Devices
INSERT INTO devices (device_id, name, room, type, status) VALUES
-- Bathroom
('bath_light', 'Light System', 'bathroom', 'light', 0),
('bath_fire', 'Fire Alert', 'bathroom', 'sensor', 0),
('bath_heater', 'Water Heater', 'bathroom', 'heater', 0),
('bath_fan', 'Fan System', 'bathroom', 'fan', 0),

-- Corridors
('corr_main_light', 'Main Light', 'corridors', 'light', 0),
('corr_spots', 'Spots Light', 'corridors', 'light', 0),
('corr_fire', 'Fire Alert', 'corridors', 'sensor', 0),

-- Reception
('rec_light', 'Light System', 'reception', 'light', 0),
('rec_window', 'Smart Window', 'reception', 'window', 0),
('rec_fire', 'Fire Alert', 'reception', 'sensor', 0),
('rec_sound', 'Sound System', 'reception', 'sound', 0),
('rec_ac', 'Air Condition', 'reception', 'ac', 0),

-- Outdoor
('out_camera', 'Camera System', 'outdoor', 'camera', 1),
('out_light', 'Light System', 'outdoor', 'light', 0),
('out_door', 'Smart Door', 'outdoor', 'door', 0),

-- Room 1
('r1_ac', 'Air Condition', 'room1', 'ac', 0),
('r1_tv', 'TV', 'room1', 'tv', 0),
('r1_light', 'Light System', 'room1', 'light', 0),
('r1_window', 'Smart Window', 'room1', 'window', 0),
('r1_fire', 'Fire Alert', 'room1', 'sensor', 0),
('r1_sound', 'Sound System', 'room1', 'sound', 0),

-- Kitchen
('kit_light', 'Light System', 'kitchen', 'light', 0),
('kit_window', 'Smart Window', 'kitchen', 'window', 0),
('kit_fan', 'Fan System', 'kitchen', 'fan', 0),
('kit_fire', 'Fire Alert', 'kitchen', 'sensor', 0),

-- Room 2
('r2_ac', 'Air Condition', 'room2', 'ac', 0),
('r2_sound', 'Sound System', 'room2', 'sound', 0),
('r2_light', 'Light System', 'room2', 'light', 0),
('r2_fire', 'Fire Alert', 'room2', 'sensor', 0);

-- Insert Sample Automation Rules
INSERT INTO automation_rules (rule_name, condition, action, priority, enabled) VALUES
('Night Mode', 'time > 22:00 AND motion_detected = 0', 'turn_off_all_lights', 1, 1),
('Morning Routine', 'time = 07:00 AND day IN (1,2,3,4,5)', 'turn_on_bathroom_light,turn_on_kitchen_light', 2, 1),
('High Temperature', 'temperature > 28 AND user_present = 1', 'turn_on_ac', 3, 1),
('Fire Emergency', 'smoke_detected = 1', 'open_all_windows,trigger_alarm', 10, 1),
('Energy Saving', 'motion_detected = 0 FOR 10 minutes', 'turn_off_lights_in_room', 1, 1),
('Welcome Home', 'door_opened = 1 AND time > 18:00', 'turn_on_reception_light,turn_on_corridors_light', 2, 1);

-- Insert Sample Sensor Data (Last 24 hours)
INSERT INTO sensors_log (sensor_type, value, room, timestamp) VALUES
-- Temperature readings
('temperature', 22.5, 'reception', datetime('now', '-24 hours')),
('temperature', 23.1, 'reception', datetime('now', '-23 hours')),
('temperature', 24.2, 'reception', datetime('now', '-22 hours')),
('temperature', 25.8, 'reception', datetime('now', '-21 hours')),
('temperature', 27.3, 'reception', datetime('now', '-20 hours')),
('temperature', 28.9, 'reception', datetime('now', '-19 hours')),
('temperature', 29.5, 'reception', datetime('now', '-18 hours')),
('temperature', 28.2, 'reception', datetime('now', '-17 hours')),
('temperature', 26.7, 'reception', datetime('now', '-16 hours')),
('temperature', 25.1, 'reception', datetime('now', '-15 hours')),

-- Humidity readings
('humidity', 45.2, 'bathroom', datetime('now', '-24 hours')),
('humidity', 48.5, 'bathroom', datetime('now', '-20 hours')),
('humidity', 52.3, 'bathroom', datetime('now', '-16 hours')),
('humidity', 49.1, 'bathroom', datetime('now', '-12 hours')),
('humidity', 46.8, 'bathroom', datetime('now', '-8 hours')),

-- Motion detection
('motion', 1, 'corridors', datetime('now', '-2 hours')),
('motion', 0, 'corridors', datetime('now', '-1 hours')),
('motion', 1, 'kitchen', datetime('now', '-30 minutes')),
('motion', 1, 'room1', datetime('now', '-15 minutes'));

-- Insert Sample Device Events
INSERT INTO device_events (device_id, event_type, old_status, new_status, triggered_by, timestamp) VALUES
('rec_light', 'toggle', 0, 1, 'user', datetime('now', '-3 hours')),
('rec_light', 'toggle', 1, 0, 'user', datetime('now', '-2 hours')),
('r1_ac', 'toggle', 0, 1, 'ai', datetime('now', '-4 hours')),
('r1_tv', 'toggle', 0, 1, 'user', datetime('now', '-5 hours')),
('r1_tv', 'toggle', 1, 0, 'user', datetime('now', '-3 hours')),
('kit_light', 'toggle', 0, 1, 'user', datetime('now', '-6 hours')),
('kit_light', 'toggle', 1, 0, 'ai', datetime('now', '-5 hours')),
('bath_heater', 'toggle', 0, 1, 'user', datetime('now', '-8 hours')),
('bath_heater', 'toggle', 1, 0, 'user', datetime('now', '-7 hours'));

-- Insert Sample User Commands
INSERT INTO user_commands (command_text, interpreted_intent, executed_action, success, timestamp) VALUES
('Turn on the living room lights', 'turn_on_light', 'rec_light:ON', 1, datetime('now', '-3 hours')),
('Make it cooler in bedroom', 'turn_on_ac', 'r1_ac:ON', 1, datetime('now', '-4 hours')),
('Turn off all lights', 'turn_off_all_lights', 'all_lights:OFF', 1, datetime('now', '-2 hours')),
('Open the kitchen window', 'open_window', 'kit_window:OPEN', 1, datetime('now', '-5 hours')),
('I am going to sleep', 'night_mode', 'night_routine:EXECUTED', 1, datetime('now', '-10 hours'));

-- Insert Sample AI Learning Data (Pattern Recognition)
INSERT INTO ai_learning_data (hour, day_of_week, temperature, humidity, motion_detected, user_present, device_id, device_status, timestamp) VALUES
-- Morning pattern (7-9 AM, weekdays)
(7, 1, 22.5, 45, 1, 1, 'bath_light', 1, datetime('now', '-72 hours')),
(7, 2, 23.1, 46, 1, 1, 'bath_light', 1, datetime('now', '-48 hours')),
(7, 3, 22.8, 44, 1, 1, 'bath_light', 1, datetime('now', '-24 hours')),
(8, 1, 23.5, 45, 1, 1, 'kit_light', 1, datetime('now', '-72 hours')),
(8, 2, 24.1, 47, 1, 1, 'kit_light', 1, datetime('now', '-48 hours')),

-- Evening pattern (18-22 PM)
(18, 1, 26.5, 48, 1, 1, 'rec_light', 1, datetime('now', '-72 hours')),
(18, 2, 27.2, 49, 1, 1, 'rec_light', 1, datetime('now', '-48 hours')),
(19, 1, 27.8, 50, 1, 1, 'r1_tv', 1, datetime('now', '-72 hours')),
(19, 2, 28.1, 51, 1, 1, 'r1_tv', 1, datetime('now', '-48 hours')),

-- Night pattern (22-24 PM)
(22, 1, 25.5, 47, 0, 1, 'rec_light', 0, datetime('now', '-72 hours')),
(22, 2, 25.8, 48, 0, 1, 'rec_light', 0, datetime('now', '-48 hours')),
(23, 1, 24.5, 46, 0, 0, 'r1_light', 0, datetime('now', '-72 hours')),
(23, 2, 24.2, 45, 0, 0, 'r1_light', 0, datetime('now', '-48 hours'));

-- Insert Sample Energy Usage Data
INSERT INTO energy_usage (device_id, power_watts, duration_minutes, total_kwh, cost, timestamp) VALUES
('r1_ac', 1500, 180, 4.5, 0.675, datetime('now', '-4 hours')),
('rec_ac', 1500, 120, 3.0, 0.450, datetime('now', '-6 hours')),
('bath_heater', 2000, 60, 2.0, 0.300, datetime('now', '-8 hours')),
('r1_tv', 150, 240, 0.6, 0.090, datetime('now', '-5 hours')),
('rec_light', 60, 300, 0.3, 0.045, datetime('now', '-3 hours')),
('kit_light', 60, 180, 0.18, 0.027, datetime('now', '-6 hours')),
('bath_fan', 75, 90, 0.1125, 0.017, datetime('now', '-7 hours'));

-- Insert Sample Alerts
INSERT INTO alerts (alert_type, severity, message, room, resolved, timestamp) VALUES
('high_temperature', 'warning', 'Temperature exceeded 30°C', 'reception', 1, datetime('now', '-12 hours')),
('energy_spike', 'info', 'Energy usage 20% above average', NULL, 1, datetime('now', '-8 hours')),
('device_offline', 'warning', 'Camera system not responding', 'outdoor', 1, datetime('now', '-6 hours')),
('motion_detected', 'info', 'Motion detected in corridors at night', 'corridors', 1, datetime('now', '-4 hours'));
