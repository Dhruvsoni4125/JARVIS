import csv
import sqlite3

conn= sqlite3.connect('JARVIS.db')

cursor= conn.cursor()
# query = ('''CREATE TABLE IF NOT EXISTS contacts(id integer primary key, name VARCHAR(200), mobile_no VARCHAR(255), email VARCHAR(255) NULL)''')
# cursor.execute(query)


# desired_columns_indices = [0, 21]
# # # Read data from CSV and insert into SQLite table for the desired columns
# with open('contacts.csv', 'r', encoding='utf-8') as csvfile:
#     csvreader = csv.reader(csvfile)
#     for row in csvreader:
#         selected_data = [row[i] for i in desired_columns_indices]
#         cursor.execute(''' INSERT INTO contacts (id, 'name', 'mobile_no') VALUES (null, ?, ?);''', tuple(selected_data))


# query= 'Aksh'
# query= query.strip().lower()

# cursor.execute('SELECT mobile_no FROM contacts WHERE LOWER(name) LIKE  ? OR LOWER(name) LIKE ?', ('%' + query + '%', query + '%'))
# result= cursor.fetchall()
# print(result[0][0])
# conn.commit()
# conn.close()