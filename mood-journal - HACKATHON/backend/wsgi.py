#!/usr/bin/env python3
"""
WSGI entry point for production deployment
This file is used by production WSGI servers like Gunicorn or Waitress
"""

import os
from . import create_app

# Create the Flask application instance
app = create_app()

if __name__ == "__main__":
    # For development, you can run this directly
    app.run(host='0.0.0.0', port=5000)
