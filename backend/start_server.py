#!/usr/bin/env python3

import uvicorn
import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    print("Starting Job Market Analyzer API...")
    print("Server will be available at: http://127.0.0.1:8001")
    print("API Documentation: http://127.0.0.1:8001/docs")
    print("Press Ctrl+C to stop the server")
    print("-" * 50)
    
    try:
        uvicorn.run(
            "app.main:app",
            host="127.0.0.1",
            port=8001,
            reload=False,  # Disable reload to see errors clearly
            log_level="info"
        )
    except Exception as e:
        print(f"Error starting server: {e}")
        import traceback
        traceback.print_exc() 