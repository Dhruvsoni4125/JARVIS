import sqlite3

# Check contacts table
conn = sqlite3.connect('JARVIS.db')
cursor = conn.cursor()

try:
    # Check if table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    print("Available tables:", tables)
    
    # Check contacts
    cursor.execute("SELECT COUNT(*) FROM contacts")
    count = cursor.fetchone()[0]
    print(f"Number of contacts: {count}")
    
    if count > 0:
        cursor.execute("SELECT name, mobile_no FROM contacts LIMIT 3")
        contacts = cursor.fetchall()
        print("Sample contacts:")
        for name, mobile in contacts:
            print(f"  {name}: {mobile}")
    else:
        print("No contacts found!")
        
except Exception as e:
    print(f"Database error: {e}")
    
conn.close()