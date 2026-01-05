import csv
import sqlite3

conn= sqlite3.connect('JARVIS.db')

cursor= conn.cursor()

# Create contacts table if it doesn't exist
query = '''CREATE TABLE IF NOT EXISTS contacts(id integer primary key, name VARCHAR(200), mobile_no VARCHAR(255), email VARCHAR(255) NULL)'''
cursor.execute(query)

# Import contacts from CSV file
desired_columns_indices = [0, 21]  # Adjust these indices based on your CSV structure

try:
    # Read data from CSV and insert into SQLite table for the desired columns
    with open('contacts.csv', 'r', encoding='utf-8') as csvfile:
        csvreader = csv.reader(csvfile)
        
        # Skip header row if it exists
        header = next(csvreader, None)
        print(f"CSV columns: {len(header) if header else 'No header found'}")
        
        contact_count = 0
        for row in csvreader:
            if len(row) > max(desired_columns_indices):
                selected_data = [row[i] for i in desired_columns_indices]
                cursor.execute(''' INSERT INTO contacts (id, 'name', 'mobile_no') VALUES (null, ?, ?);''', tuple(selected_data))
                contact_count += 1
            
        print(f"Imported {contact_count} contacts from CSV")
        
except FileNotFoundError:
    print("contacts.csv file not found. Please ensure the file exists.")
except Exception as e:
    print(f"Error importing contacts: {e}")

# Commit changes and close connection
conn.commit()
conn.close()

print("Database setup completed!")