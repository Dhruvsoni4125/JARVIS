import sqlite3

# Test contacts
conn = sqlite3.connect('JARVIS.db')
cursor = conn.cursor()

# Check contacts count
cursor.execute("SELECT COUNT(*) FROM contacts")
count = cursor.fetchone()[0]
print(f"Total contacts: {count}")

# Show first 5 contacts
if count > 0:
    cursor.execute("SELECT name, mobile_no FROM contacts LIMIT 5")
    contacts = cursor.fetchall()
    print("\\nFirst 5 contacts:")
    for name, mobile in contacts:
        print(f"  {name}: {mobile}")

conn.close()