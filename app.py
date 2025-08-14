#!/usr/bin/env python3
"""
Main entry point for the Speech Emotion Recognition web application.
This file provides a simple way to run the Streamlit app.
"""

import sys
from pathlib import Path

# Add the src directory to Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

# Import and run the main app
from ser.app import main

if __name__ == "__main__":
    main()


