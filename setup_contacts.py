#!/usr/bin/env python3
"""
Setup contacts database for JARVIS
"""

import csv
import sqlite3
import os

def setup_contacts():
    """Setup contacts table and import from CSV"""
    
    print("=== JARVIS Contacts Setup ===")
    
    # Connect to database
    conn = sqlite3.connect('JARVIS.db')
    cursor = conn.cursor()
    
    # Create table
    print("Creating contacts table...")
    query = '''CREATE TABLE IF NOT EXISTS contacts(
        id integer primary key, 
        name VARCHAR(200), 
        mobile_no VARCHAR(255), 
        email VARCHAR(255) NULL
    )'''
    cursor.execute(query)
    
    # Check if contacts.csv exists
    if not os.path.exists('contacts.csv'):
        print("❌ contacts.csv file not found!")
        print("Please ensure contacts.csv is in the project directory")
        return False
    
    # Read first few lines to understand CSV structure
    print("Analyzing CSV file...")
    with open('contacts.csv', 'r', encoding='utf-8') as csvfile:
        csvreader = csv.reader(csvfile)
        
        # Read header
        try:
            header = next(csvreader)
            print(f"✓ CSV has {len(header)} columns")
            print("First 10 columns:")
            for i, col in enumerate(header[:10]):
                print(f"  {i}: {col}")
            
            # Read first data row
            first_row = next(csvreader)
            print(f"\\nFirst data row ({len(first_row)} values):")
            for i, val in enumerate(first_row[:10]):
                print(f"  {i}: {val}")
                
        except Exception as e:
            print(f"❌ Error reading CSV: {e}")
            return False
    
    # Ask user for column indices
    print("\\n" + "="*50)
    print("Please identify the correct column indices:")
    print("- Which column contains the NAME? (enter number)")
    print("- Which column contains the MOBILE NUMBER? (enter number)")
    
    try:
        name_col = int(input("Name column index: "))
        mobile_col = int(input("Mobile column index: "))
    except:
        print("Using default: name=0, mobile=21")
        name_col = 0
        mobile_col = 21
    
    # Import contacts
    print(f"\\nImporting contacts using columns {name_col} (name) and {mobile_col} (mobile)...")
    
    contact_count = 0
    error_count = 0
    
    with open('contacts.csv', 'r', encoding='utf-8') as csvfile:
        csvreader = csv.reader(csvfile)
        
        # Skip header
        next(csvreader, None)
        
        for row_num, row in enumerate(csvreader, 1):
            try:
                if len(row) > max(name_col, mobile_col):
                    name = row[name_col].strip()
                    mobile = row[mobile_col].strip()
                    
                    if name and mobile:  # Only import if both name and mobile exist
                        cursor.execute(
                            'INSERT INTO contacts (name, mobile_no) VALUES (?, ?)', 
                            (name, mobile)
                        )
                        contact_count += 1
                    
                        # Show progress every 100 contacts
                        if contact_count % 100 == 0:
                            print(f"Imported {contact_count} contacts...")
                            
            except Exception as e:
                error_count += 1
                if error_count <= 5:  # Show first 5 errors
                    print(f"Error on row {row_num}: {e}")
    
    # Commit and close
    conn.commit()
    conn.close()
    
    print(f"\\n✓ Successfully imported {contact_count} contacts")
    if error_count > 0:
        print(f"⚠️  {error_count} rows had errors and were skipped")
    
    return contact_count > 0

def test_contacts():
    """Test if contacts can be found"""
    
    print("\\n=== Testing Contact Search ===")
    
    conn = sqlite3.connect('JARVIS.db')
    cursor = conn.cursor()
    
    # Count total contacts
    cursor.execute("SELECT COUNT(*) FROM contacts")
    total = cursor.fetchone()[0]
    print(f"Total contacts in database: {total}")
    
    if total > 0:
        # Show sample contacts
        cursor.execute("SELECT name, mobile_no FROM contacts LIMIT 5")
        contacts = cursor.fetchall()
        print("\\nSample contacts:")
        for name, mobile in contacts:
            print(f"  {name}: {mobile}")
        
        # Test search functionality
        print("\\nTesting search...")
        test_name = contacts[0][0].split()[0].lower()  # Use first word of first contact
        cursor.execute(
            "SELECT name, mobile_no FROM contacts WHERE LOWER(name) LIKE ?", 
            (f'%{test_name}%',)
        )
        results = cursor.fetchall()
        print(f"Search for '{test_name}' found {len(results)} results")
        
    conn.close()

if __name__ == "__main__":
    if setup_contacts():
        test_contacts()
        print("\\n🎉 Setup completed! Your WhatsApp commands should now work.")
        print("Try: 'Send message to [contact name]'")
    else:
        print("\\n❌ Setup failed. Please check the errors above.")