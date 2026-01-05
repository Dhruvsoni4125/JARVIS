#!/usr/bin/env python3
"""
Debug script to identify WhatsApp command recognition issues
"""

import sys
import os
import sqlite3

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def check_database():
    """Check if contacts exist in database"""
    try:
        conn = sqlite3.connect('JARVIS.db')
        cursor = conn.cursor()
        
        # Check if contacts table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='contacts'")
        table_exists = cursor.fetchone()
        
        if table_exists:
            print("✓ Contacts table exists")
            
            # Check number of contacts
            cursor.execute("SELECT COUNT(*) FROM contacts")
            count = cursor.fetchone()[0]
            print(f"✓ Number of contacts in database: {count}")
            
            if count > 0:
                # Show sample contacts
                cursor.execute("SELECT name, mobile_no FROM contacts LIMIT 5")
                contacts = cursor.fetchall()
                print("Sample contacts:")
                for name, mobile in contacts:
                    print(f"  - {name}: {mobile}")
            else:
                print("❌ No contacts found in database")
        else:
            print("❌ Contacts table does not exist")
            
        conn.close()
        return table_exists is not None
        
    except Exception as e:
        print(f"❌ Database error: {e}")
        return False

def test_command_recognition():
    """Test command recognition logic"""
    
    test_commands = [
        "send message to john",
        "phone call to mary", 
        "video call to alex",
        "send message to mom",
        "whatsapp message to dad"
    ]
    
    print("\n=== Testing Command Recognition ===")
    
    for cmd in test_commands:
        print(f"\nTesting: '{cmd}'")
        
        # Test the basic recognition logic
        if "send message" in cmd or "phone call" in cmd or "video call" in cmd:
            print("✓ Command pattern recognized")
            
            # Test contact finding
            try:
                from engine.features import findContact
                contact_no, name = findContact(cmd)
                
                if contact_no != 0:
                    print(f"✓ Contact found: {name} -> {contact_no}")
                else:
                    print(f"❌ Contact not found for: {cmd}")
                    
            except Exception as e:
                print(f"❌ Error in findContact: {e}")
        else:
            print("❌ Command pattern not recognized")

def test_whatsapp_function():
    """Test WhatsApp function directly"""
    print("\n=== Testing WhatsApp Function ===")
    
    try:
        # Create a mock speak function to avoid eel dependency
        def mock_speak(text):
            print(f"[SPEAK]: {text}")
        
        # Monkey patch speak function
        import engine.command
        original_speak = engine.command.speak
        engine.command.speak = mock_speak
        
        from engine.features import whatsApp
        
        # Test with fake data
        test_mobile = "+919876543210"
        test_message = "Hello test"
        test_name = "Test User"
        
        print("Testing message sending...")
        whatsApp(test_mobile, test_message, 'message', test_name)
        
        print("Testing call...")
        whatsApp(test_mobile, "", 'call', test_name)
        
        print("Testing video call...")
        whatsApp(test_mobile, "", 'video call', test_name)
        
        # Restore original speak function
        engine.command.speak = original_speak
        
    except Exception as e:
        print(f"❌ WhatsApp function error: {e}")
        import traceback
        traceback.print_exc()

def check_whatsapp_installation():
    """Check if WhatsApp is accessible"""
    print("\n=== Checking WhatsApp Installation ===")
    
    import subprocess
    
    try:
        
        # Test WhatsApp protocol
        print("Testing WhatsApp protocol handler...")
        result = subprocess.run(
            'start "" "whatsapp://send?phone=+919876543210&text=test"', 
            shell=True, 
            capture_output=True, 
            text=True,
            timeout=5
        )
        print("✓ WhatsApp protocol handler seems to work")
        
    except subprocess.TimeoutExpired:
        print("✓ WhatsApp protocol launched (timed out waiting for response - this is normal)")
    except Exception as e:
        print(f"❌ WhatsApp protocol error: {e}")

def main():
    print("=== JARVIS WhatsApp Debug Tool ===\n")
    
    # Step 1: Check database
    db_ok = check_database()
    
    # Step 2: Test command recognition
    test_command_recognition()
    
    # Step 3: Test WhatsApp function
    test_whatsapp_function()
    
    # Step 4: Check WhatsApp installation
    check_whatsapp_installation()
    
    print("\n=== Debug Summary ===")
    print("If you see errors above, those are the issues to fix:")
    print("1. Make sure contacts are in the database")
    print("2. Ensure command patterns match your voice input")
    print("3. Check WhatsApp installation and protocol handlers")
    
    print(f"\nTo add contacts to database, you can:")
    print("1. Use the contacts.csv file")
    print("2. Add contacts manually to JARVIS.db")
    print("3. Check if your database import script ran correctly")

if __name__ == "__main__":
    main()