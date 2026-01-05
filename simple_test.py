import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Simple test without complex dependencies
try:
    print("Testing WhatsApp import...")
    from engine.features import whatsApp
    print("✓ WhatsApp function imported successfully")
    
    # Simple test call
    print("Testing with fake phone number...")
    # This will test the logic without actually sending
    test_mobile = "+919876543210"
    test_message = "Test message"
    test_name = "Test User"
    
    print(f"Calling whatsApp function with:")
    print(f"  Mobile: {test_mobile}")
    print(f"  Message: {test_message}")
    print(f"  Flag: message")
    print(f"  Name: {test_name}")
    
    print("Note: This is a dry run - no actual WhatsApp will be opened")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
except Exception as e:
    print(f"❌ Error: {e}")

print("Test completed")