import sys
import os

script_directory = os.path.dirname(os.path.realpath(__file__))

sys.path.append(script_directory)
from .SyncPulse import main

if __name__ == "__main__":
    main()
