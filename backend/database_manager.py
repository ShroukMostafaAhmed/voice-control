"""
Async Database Manager for Smart Home
"""

import aiosqlite
from typing import List, Dict, Optional
from datetime import datetime

class DatabaseManager:
    def __init__(self, db_path='../database/smart_home.db'):
        self.db_path = db_path
        self.conn = None
    
    async def initialize(self):
        """Initialize database connection"""
        self.conn = await aiosqlite.connect(self.db_path)
        self.conn.row_factory = aiosqlite.Row
        print(f"✓ Database connected: {self.db_path}")
    
    async def close(self):
        """Close database connection"""
        if self.conn:
            await self.conn.close()
    
    # ==================== DEVICE OPERATIONS ====================
    
    async def get_all_devices(self) -> List[Dict]:
        """Get all devices"""
        async with self.conn.execute("SELECT * FROM devices") as cursor:
            rows = await cursor.fetchall()
            return [dict(row) for row in rows]
    
    async def get_device_by_id(self, device_id: str) -> Optional[Dict]:
        """Get device by ID"""
        async with self.conn.execute(
            "SELECT * FROM devices WHERE device_id = ?", (device_id,)
        ) as cursor:
            row = await cursor.fetchone()
            return dict(row) if row else None
    
    async def get_devices_by_room(self, room: str) -> List[Dict]:
        """Get all devices in a room"""
        async with self.conn.execute(
            "SELECT * FROM devices WHERE room = ?", (room,)
        ) as cursor:
            rows = await cursor.fetchall()
            return [dict(row) for row in rows]
    
    async def update_device_status(self, device_id: str, status: int, triggered_by: str = 'user'):
        """Update device status and log event"""
        # Get old status
        async with self.conn.execute(
            "SELECT status FROM devices WHERE device_id = ?", (device_id,)
        ) as cursor:
            row = await cursor.fetchone()
            old_status = row[0] if row else 0
        
        # Update status
        await self.conn.execute(
            "UPDATE devices SET status = ?, last_updated = CURRENT_TIMESTAMP WHERE device_id = ?",
            (status, device_id)
        )
        
        # Log event
        await self.conn.execute(
            "INSERT INTO device_events (device_id, event_type, old_status, new_status, triggered_by) VALUES (?, ?, ?, ?, ?)",
            (device_id, 'toggle', old_status, status, triggered_by)
        )
        
        await self.conn.commit()
    
    # ==================== SENSOR OPERATIONS ====================
    
    async def log_sensor_data(self, sensor_type: str, value: float, room: str):
        """Log sensor reading"""
        await self.conn.execute(
            "INSERT INTO sensors_log (sensor_type, value, room) VALUES (?, ?, ?)",
            (sensor_type, value, room)
        )
        await self.conn.commit()
    
    async def get_latest_sensor_data(self, sensor_type: str, room: Optional[str] = None) -> Optional[Dict]:
        """Get latest sensor reading"""
        if room:
            query = "SELECT * FROM sensors_log WHERE sensor_type = ? AND room = ? ORDER BY timestamp DESC LIMIT 1"
            params = (sensor_type, room)
        else:
            query = "SELECT * FROM sensors_log WHERE sensor_type = ? ORDER BY timestamp DESC LIMIT 1"
            params = (sensor_type,)
        
        async with self.conn.execute(query, params) as cursor:
            row = await cursor.fetchone()
            return dict(row) if row else None
    
    async def get_sensor_history(self, sensor_type: str, hours: int = 24) -> List[Dict]:
        """Get sensor history"""
        async with self.conn.execute(
            "SELECT * FROM sensors_log WHERE sensor_type = ? AND timestamp > datetime('now', '-' || ? || ' hours') ORDER BY timestamp DESC",
            (sensor_type, hours)
        ) as cursor:
            rows = await cursor.fetchall()
            return [dict(row) for row in rows]
    
    # ==================== AI LEARNING DATA ====================
    
    async def log_ai_learning_data(self, hour: int, day_of_week: int, temperature: float,
                                   humidity: float, motion_detected: int, user_present: int,
                                   device_id: str, device_status: int):
        """Log data for AI learning"""
        await self.conn.execute(
            """INSERT INTO ai_learning_data 
            (hour, day_of_week, temperature, humidity, motion_detected, user_present, device_id, device_status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (hour, day_of_week, temperature, humidity, motion_detected, user_present, device_id, device_status)
        )
        await self.conn.commit()
    
    async def get_ai_training_data(self, days: int = 30) -> List[Dict]:
        """Get AI training data"""
        async with self.conn.execute(
            "SELECT * FROM ai_learning_data WHERE timestamp > datetime('now', '-' || ? || ' days') ORDER BY timestamp",
            (days,)
        ) as cursor:
            rows = await cursor.fetchall()
            return [dict(row) for row in rows]
    
    async def get_device_usage_pattern(self, device_id: str) -> List[Dict]:
        """Get usage pattern for a device"""
        async with self.conn.execute(
            """SELECT hour, day_of_week, AVG(device_status) as avg_status, COUNT(*) as count
            FROM ai_learning_data 
            WHERE device_id = ?
            GROUP BY hour, day_of_week
            ORDER BY hour, day_of_week""",
            (device_id,)
        ) as cursor:
            rows = await cursor.fetchall()
            return [dict(row) for row in rows]
    
    # ==================== AUTOMATION RULES ====================
    
    async def get_active_rules(self) -> List[Dict]:
        """Get all active automation rules"""
        async with self.conn.execute(
            "SELECT * FROM automation_rules WHERE enabled = 1 ORDER BY priority DESC"
        ) as cursor:
            rows = await cursor.fetchall()
            return [dict(row) for row in rows]
    
    async def add_automation_rule(self, rule_name: str, condition: str, action: str, priority: int = 1):
        """Add new automation rule"""
        await self.conn.execute(
            "INSERT INTO automation_rules (rule_name, condition, action, priority) VALUES (?, ?, ?, ?)",
            (rule_name, condition, action, priority)
        )
        await self.conn.commit()
    
    # ==================== ENERGY TRACKING ====================
    
    async def log_energy_usage(self, device_id: str, power_watts: float, duration_minutes: float, cost: float = None):
        """Log energy usage"""
        total_kwh = (power_watts * duration_minutes) / 60000
        if cost is None:
            cost = total_kwh * 0.15
        
        await self.conn.execute(
            "INSERT INTO energy_usage (device_id, power_watts, duration_minutes, total_kwh, cost) VALUES (?, ?, ?, ?, ?)",
            (device_id, power_watts, duration_minutes, total_kwh, cost)
        )
        await self.conn.commit()
    
    async def get_energy_report(self, days: int = 7) -> Dict:
        """Get energy usage report"""
        async with self.conn.execute(
            """SELECT 
                COALESCE(SUM(total_kwh), 0) as total_kwh,
                COALESCE(SUM(cost), 0) as total_cost,
                COUNT(DISTINCT device_id) as devices_used
            FROM energy_usage 
            WHERE timestamp > datetime('now', '-' || ? || ' days')""",
            (days,)
        ) as cursor:
            row = await cursor.fetchone()
            return dict(row) if row else {}
    
    # ==================== ALERTS ====================
    
    async def create_alert(self, alert_type: str, severity: str, message: str, room: Optional[str] = None):
        """Create new alert"""
        await self.conn.execute(
            "INSERT INTO alerts (alert_type, severity, message, room) VALUES (?, ?, ?, ?)",
            (alert_type, severity, message, room)
        )
        await self.conn.commit()
    
    async def get_unresolved_alerts(self) -> List[Dict]:
        """Get all unresolved alerts"""
        async with self.conn.execute(
            "SELECT * FROM alerts WHERE resolved = 0 ORDER BY timestamp DESC"
        ) as cursor:
            rows = await cursor.fetchall()
            return [dict(row) for row in rows]
    
    # ==================== AI HELPER FUNCTIONS ====================
    
    async def get_current_state_for_ai(self) -> Dict:
        """Get current system state for AI"""
        devices = await self.get_all_devices()
        temp = await self.get_latest_sensor_data('temperature')
        humidity = await self.get_latest_sensor_data('humidity')
        motion = await self.get_latest_sensor_data('motion')
        
        now = datetime.now()
        
        return {
            'timestamp': now.isoformat(),
            'hour': now.hour,
            'day_of_week': now.weekday(),
            'temperature': temp['value'] if temp else 25.0,
            'humidity': humidity['value'] if humidity else 50.0,
            'motion_detected': int(motion['value']) if motion else 0,
            'devices': devices
        }
    
    async def get_device_statistics(self) -> List[Dict]:
        """Get device usage statistics"""
        async with self.conn.execute("""
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
        """) as cursor:
            rows = await cursor.fetchall()
            return [dict(row) for row in rows]
