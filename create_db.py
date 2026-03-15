import sqlite3

conn = sqlite3.connect("notes.db")

conn.execute("""
CREATE TABLE IF NOT EXISTS notes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    subject TEXT NOT NULL,
    semester TEXT NOT NULL,
    filename TEXT NOT NULL
)
""")

conn.close()
print("Database and table created successfully!")