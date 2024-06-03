# agentic_employment_wrapper.py

import sys
import os

# Add the directory containing app.py to the system path
sys.path.insert(0, os.path.dirname(__file__))

from app import main

if __name__ == "__main__":
    main()
