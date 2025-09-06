#!/usr/bin/env python3
"""
Simple script to run the Mood Journal backend Flask application
"""

import os
import sys

# Add the parent directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend import create_app

if __name__ == '__main__':
    # Create the Flask application
    app = create_app()
    
    # Run the application
    print("Starting Mood Journal Backend...")
    print("Server will be available at: http://localhost:5000")
    print("Press Ctrl+C to stop the server")
    
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )
