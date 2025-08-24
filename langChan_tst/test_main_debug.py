"""
Test the main CLI with proper error handling
"""

import sys
import traceback
from pathlib import Path

# Add project to path
sys.path.insert(0, str(Path(__file__).parent))

try:
    from main import main
    print("✅ Main function imported successfully")
    
    # Test the main function directly
    sys.argv = ["main.py", "--version"]
    result = main()
    print(f"✅ Main function executed, result: {result}")
    
except SystemExit as e:
    print(f"✅ System exit (normal): {e.code}")
except Exception as e:
    print(f"❌ Error: {e}")
    traceback.print_exc()
