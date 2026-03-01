#!/usr/bin/env python3
"""
Initialize SQLite Database for Smart Home System
"""

import sqlite3
import os
from datetime import datetime

def init_database(db_path='smart_home.db'):
    """Initialize the database with schema and seed data"""
    
    # Remove existing database if exists
    if os.path.exists(db_path):
        print(f"Removing existing database: {db_path}")
        os.remove(db_path)
    
    # Create connection
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print(f"Creating database: {db_path}")
    
    # Read and execute schema
    with open('schema.sql', 'r', encoding='utf-8') as f:
        schema_sql = f.read()
        cursor.executescript(schema_sql)
    
    print("✓ Schema created successfully")
    
    # Read and execute seed data
    with open('seed_data.sql', 'r', encoding='utf-8') as f:
        seed_sql = f.read()
        cursor.executescript(seed_sql)
    
    print("✓ Seed data inserted successfully")
    
    # Commit and close
    conn.commit()
    
    # Print statistics
    cursor.execute("SELECT COUNT(*) FROM devices")
    device_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM sensors_log")
    sensor_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM device_events")
    event_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM ai_learning_data")
    learning_count = cursor.fetchone()[0]
    
    print(f"\nDatabase Statistics:")
    print(f"   - Devices: {device_count}")
    print(f"   - Sensor Logs: {sensor_count}")
    print(f"   - Device Events: {event_count}")
    print(f"   - AI Learning Data: {learning_count}")
    
    conn.close()
    print(f"\nDatabase initialized successfully: {db_path}")

if __name__ == "__main__":
    init_database()
