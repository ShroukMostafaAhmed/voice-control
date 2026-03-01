#!/usr/bin/env python3
"""
Run AI System
"""

import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    from ai_api import app
    import uvicorn
    
    print("=" * 60)
    print("Smart Home AI System")
    print("=" * 60)
    print("\nStarting AI API Server...")
    print("   - API: http://localhost:8090")
    print("   - Docs: http://localhost:8090/docs")
    print("\nTry these commands:")
    print("   - 'Turn on reception light'")
    print("   - 'Turn off kitchen fan'")
    print("   - 'Open bedroom window'")
    print("\nFeatures:")
    print("   - Virtual Devices Simulation")
    print("   - AI Decision Engine")
    print("   - Natural Language Commands")
    print("   - Auto Automation Rules")
    print("\n" + "=" * 60 + "\n")
    
    uvicorn.run(app, host="0.0.0.0", port=8090, log_level="info")
