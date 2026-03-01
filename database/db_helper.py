#!/usr/bin/env python3
"""
Database Helper Functions for Smart Home System
Easy to use with AI models
"""

import sqlite3
import json
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional

class SmartHomeDB:
    def __init__(self, db_path='smart_home.db'):
        self.db_path = db_path
    
    def get_connection(self):
        """Get database connection"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    # ==================== DEVICE OPERATIONS ====================
    
    def get_all_devices(self) -> List[Dict]:
        """Get all devices"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM devices")
        devices = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return devices
    
    def get_device_by_id(self, device_id: str) -> Optional[Dict]:
        """Get device by ID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM devices WHERE device_id = ?", (device_id,))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None
    
    def get_devices_by_room(self, room: str) -> List[Dict]:
        """Get all devices in a room"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM devices WHERE room = ?", (room,))
        devices = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return devices
    
    def update_device_status(self, device_id: str, status: int, triggered_by: str = 'user'):
        """Update device status and log event"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Get old status
        cursor.execute("SELECT status FROM devices WHERE device_id = ?", (device_id,))
        old_status = cursor.fetchone()[0]
        
        # Update status
        cursor.execute(
            "UPDATE devices SET status = ?, last_updated = CURRENT_TIMESTAMP WHERE device_id = ?",
            (status, device_id)
        )
        
        # Log event
        cursor.execute(
            "INSERT INTO device_events (device_id, event_type, old_status, new_status, triggered_by) VALUES (?, ?, ?, ?, ?)",
            (device_id, 'toggle', old_status, status, triggered_by)
        )
        
        conn.commit()
        conn.close()
    
    # ==================== SENSOR OPERATIONS ====================
    
    def log_sensor_data(self, sensor_type: str, value: float, room: str):
        """Log sensor reading"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO sensors_log (sensor_type, value, room) VALUES (?, ?, ?)",
            (sensor_type, value, room)
        )
        conn.commit()
        conn.close()
    
    def get_latest_sensor_data(self, sensor_type: str, room: Optional[str] = None) -> Optional[Dict]:
        """Get latest sensor reading"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        if room:
            cursor.execute(
                "SELECT * FROM sensors_log WHERE sensor_type = ? AND room = ? ORDER BY timestamp DESC LIMIT 1",
                (sensor_type, room)
            )
        else:
            cursor.execute(
                "SELECT * FROM sensors_log WHERE sensor_type = ? ORDER BY timestamp DESC LIMIT 1",
                (sensor_type,)
            )
        
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None
    
    def get_sensor_history(self, sensor_type: str, hours: int = 24) -> List[Dict]:
        """Get sensor history for last N hours"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM sensors_log WHERE sensor_type = ? AND timestamp > datetime('now', '-' || ? || ' hours') ORDER BY timestamp DESC",
            (sensor_type, hours)
        )
        data = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return data
    
    # ==================== AI LEARNING DATA ====================
    
    def log_ai_learning_data(self, hour: int, day_of_week: int, temperature: float, 
                            humidity: float, motion_detected: int, user_present: int,
                            device_id: str, device_status: int):
        """Log data for AI learning"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """INSERT INTO ai_learning_data 
            (hour, day_of_week, temperature, humidity, motion_detected, user_present, device_id, device_status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (hour, day_of_week, temperature, humidity, motion_detected, user_present, device_id, device_status)
        )
        conn.commit()
        conn.close()
    
    def get_ai_training_data(self, days: int = 30) -> List[Dict]:
        """Get AI training data for last N days"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM ai_learning_data WHERE timestamp > datetime('now', '-' || ? || ' days') ORDER BY timestamp",
            (days,)
        )
        data = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return data
    
    def get_device_usage_pattern(self, device_id: str) -> List[Dict]:
        """Get usage pattern for a device (for AI prediction)"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """SELECT hour, day_of_week, AVG(device_status) as avg_status, COUNT(*) as count
            FROM ai_learning_data 
            WHERE device_id = ?
            GROUP BY hour, day_of_week
            ORDER BY hour, day_of_week""",
            (device_id,)
        )
        data = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return data
    
    # ==================== AUTOMATION RULES ====================
    
    def get_active_rules(self) -> List[Dict]:
        """Get all active automation rules"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM automation_rules WHERE enabled = 1 ORDER BY priority DESC")
        rules = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return rules
    
    def add_automation_rule(self, rule_name: str, condition: str, action: str, priority: int = 1):
        """Add new automation rule"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO automation_rules (rule_name, condition, action, priority) VALUES (?, ?, ?, ?)",
            (rule_name, condition, action, priority)
        )
        conn.commit()
        conn.close()
    
    # ==================== ENERGY TRACKING ====================
    
    def log_energy_usage(self, device_id: str, power_watts: float, duration_minutes: float, cost: float = None):
        """Log energy usage"""
        total_kwh = (power_watts * duration_minutes) / 60000
        if cost is None:
            cost = total_kwh * 0.15  # Default rate
        
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO energy_usage (device_id, power_watts, duration_minutes, total_kwh, cost) VALUES (?, ?, ?, ?, ?)",
            (device_id, power_watts, duration_minutes, total_kwh, cost)
        )
        conn.commit()
        conn.close()
    
    def get_energy_report(self, days: int = 7) -> Dict:
        """Get energy usage report"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            """SELECT 
                SUM(total_kwh) as total_kwh,
                SUM(cost) as total_cost,
                COUNT(DISTINCT device_id) as devices_used
            FROM energy_usage 
            WHERE timestamp > datetime('now', '-' || ? || ' days')""",
            (days,)
        )
        
        report = dict(cursor.fetchone())
        conn.close()
        return report
    
    # ==================== ALERTS ====================
    
    def create_alert(self, alert_type: str, severity: str, message: str, room: Optional[str] = None):
        """Create new alert"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO alerts (alert_type, severity, message, room) VALUES (?, ?, ?, ?)",
            (alert_type, severity, message, room)
        )
        conn.commit()
        conn.close()
    
    def get_unresolved_alerts(self) -> List[Dict]:
        """Get all unresolved alerts"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM alerts WHERE resolved = 0 ORDER BY timestamp DESC")
        alerts = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return alerts
    
    # ==================== AI HELPER FUNCTIONS ====================
    
    def get_current_state_for_ai(self) -> Dict:
        """Get current system state formatted for AI model"""
        devices = self.get_all_devices()
        temp = self.get_latest_sensor_data('temperature')
        humidity = self.get_latest_sensor_data('humidity')
        motion = self.get_latest_sensor_data('motion')
        
        now = datetime.now()
        
        return {
            'timestamp': now.isoformat(),
            'hour': now.hour,
            'day_of_week': now.weekday(),
            'temperature': temp['value'] if temp else 25.0,
            'humidity': humidity['value'] if humidity else 50.0,
            'motion_detected': motion['value'] if motion else 0,
            'devices': devices
        }
    
    def export_training_data_json(self, output_file: str = 'training_data.json'):
        """Export training data as JSON for AI models"""
        data = self.get_ai_training_data(days=90)
        with open(output_file, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"✓ Training data exported to {output_file}")
    
    def get_device_statistics(self) -> Dict:
        """Get device usage statistics"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT 
                d.device_id,
                d.name,
                d.room,
                d.type,
                COUNT(de.id) as total_events,
                SUM(CASE WHEN de.new_status = 1 THEN 1 ELSE 0 END) as times_turned_on,
                SUM(CASE WHEN de.triggered_by = 'ai' THEN 1 ELSE 0 END) as ai_triggered
            FROM devices d
            LEFT JOIN device_events de ON d.device_id = de.device_id
            GROUP BY d.device_id
        """)
        
        stats = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return stats


# Example usage
if __name__ == "__main__":
    db = SmartHomeDB()
    
    print("=== Current System State ===")
    state = db.get_current_state_for_ai()
    print(json.dumps(state, indent=2))
    
    print("\n=== Device Statistics ===")
    stats = db.get_device_statistics()
    for stat in stats[:5]:
        print(f"{stat['name']} ({stat['room']}): {stat['total_events']} events, {stat['ai_triggered']} AI-triggered")
    
    print("\n=== Energy Report (Last 7 days) ===")
    energy = db.get_energy_report(7)
    print(f"Total Energy: {energy['total_kwh']:.2f} kWh")
    print(f"Total Cost: ${energy['total_cost']:.2f}")
