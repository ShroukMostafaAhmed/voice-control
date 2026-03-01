-- Smart Home Database Schema

-- Devices Table
CREATE TABLE IF NOT EXISTS devices (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    device_id TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    room TEXT NOT NULL,
    type TEXT NOT NULL,
    status INTEGER DEFAULT 0,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Sensors Log Table
CREATE TABLE IF NOT EXISTS sensors_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sensor_type TEXT NOT NULL,
    value REAL NOT NULL,
    room TEXT NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Device Events Table
CREATE TABLE IF NOT EXISTS device_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    device_id TEXT NOT NULL,
    event_type TEXT NOT NULL,
    old_status INTEGER,
    new_status INTEGER,
    triggered_by TEXT DEFAULT 'user',
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (device_id) REFERENCES devices(device_id)
);

-- User Commands Table
CREATE TABLE IF NOT EXISTS user_commands (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    command_text TEXT NOT NULL,
    interpreted_intent TEXT,
    executed_action TEXT,
    success INTEGER DEFAULT 1,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- AI Learning Data Table
CREATE TABLE IF NOT EXISTS ai_learning_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    hour INTEGER NOT NULL,
    day_of_week INTEGER NOT NULL,
    temperature REAL,
    humidity REAL,
    motion_detected INTEGER,
    user_present INTEGER,
    device_id TEXT NOT NULL,
    device_status INTEGER NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (device_id) REFERENCES devices(device_id)
);

-- Automation Rules Table
CREATE TABLE IF NOT EXISTS automation_rules (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    rule_name TEXT NOT NULL,
    condition TEXT NOT NULL,
    action TEXT NOT NULL,
    priority INTEGER DEFAULT 1,
    enabled INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Energy Usage Table
CREATE TABLE IF NOT EXISTS energy_usage (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    device_id TEXT NOT NULL,
    power_watts REAL NOT NULL,
    duration_minutes REAL NOT NULL,
    total_kwh REAL NOT NULL,
    cost REAL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (device_id) REFERENCES devices(device_id)
);

-- Alerts Table
CREATE TABLE IF NOT EXISTS alerts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    alert_type TEXT NOT NULL,
    severity TEXT NOT NULL,
    message TEXT NOT NULL,
    room TEXT,
    resolved INTEGER DEFAULT 0,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create Indexes for Performance
CREATE INDEX IF NOT EXISTS idx_device_events_timestamp ON device_events(timestamp);
CREATE INDEX IF NOT EXISTS idx_sensors_log_timestamp ON sensors_log(timestamp);
CREATE INDEX IF NOT EXISTS idx_ai_learning_timestamp ON ai_learning_data(timestamp);
CREATE INDEX IF NOT EXISTS idx_energy_usage_timestamp ON energy_usage(timestamp);
CREATE INDEX IF NOT EXISTS idx_device_id ON devices(device_id);
