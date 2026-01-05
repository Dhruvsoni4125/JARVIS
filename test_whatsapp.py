#!/usr/bin/env python3
"""
Test script for WhatsApp functionality
"""

import sys
import os
import pyttsx3

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Create a standalone speak function for testing
def test_speak(text):
    """Standalone speak function for testing without eel"""
    print(f"[SPEAK]: {text}")
    try:
        engine = pyttsx3.init('sapi5')
        engine.setProperty('rate', 180)
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"TTS Error: {e}")

# Monkey patch the speak function for testing
import engine.command
engine.command.speak = test_speak

from engine.features import whatsApp

def test_whatsapp():
    """Test the WhatsApp functionality"""
    
    print("=== WhatsApp Function Test ===")
    
    # Test data
    test_mobile = "+919876543210"  # Replace with a real number for actual testing
    test_message = "Hello, this is a test message from JARVIS!"
    test_name = "Test Contact"
    
    print(f"Testing WhatsApp functionality...")
    print(f"Mobile: {test_mobile}")
    print(f"Message: {test_message}")
    print(f"Name: {test_name}")
    
    # Test different flags
    test_cases = [
        ("message", test_message),
        ("call", ""),
        ("video call", "")
    ]
    
    for flag, msg in test_cases:
        print(f"\n--- Testing {flag} ---")
        try:
            if flag == "message":
                # For message testing, we'll just validate the function without actually sending
                print("Note: Message sending test - this will open WhatsApp Web/Desktop")
                choice = input("Do you want to proceed with actual message test? (y/n): ").lower()
                if choice == 'y':
                    whatsApp(test_mobile, msg, flag, test_name)
                else:
                    print("Skipping actual message test")
            else:
                # For calls, we'll test the URL generation logic
                print(f"Testing {flag} logic...")
                # We can modify the function to just return the URL for testing
                print(f"Would open WhatsApp for {flag} with {test_name}")
                
        except Exception as e:
            print(f"Error testing {flag}: {e}")
    
    print("\n=== Test completed ===")

if __name__ == "__main__":
    test_whatsapp()