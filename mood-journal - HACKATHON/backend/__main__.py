#!/usr/bin/env python3
"""
Main entry point for the Mood Journal Backend
Run this file directly to start the Flask development server
"""

import os
from . import create_app

def main():
    """Main function to run the Flask application"""
    # Set environment variables
    os.environ.setdefault('FLASK_ENV', 'development')
    
    # Create and configure the Flask app
    app = create_app()
    
    # Run the application
    if __name__ == '__main__':
        app.run(
            host='0.0.0.0',
            port=5000,
            debug=True
        )

if __name__ == '__main__':
    main()
