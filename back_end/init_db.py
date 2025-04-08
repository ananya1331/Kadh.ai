import sqlite3

with open("schema.sql", "r") as f:
    schema = f.read()

conn = sqlite3.connect("kadhai.db")
cursor = conn.cursor()

try:
    cursor.executescript(schema)
    print("Database created and schema loaded successfully.")
except sqlite3.OperationalError as e:
    print("Error:", e)

conn.commit()
conn.close()
