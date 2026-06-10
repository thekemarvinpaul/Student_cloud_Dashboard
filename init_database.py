import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

cursor.execute("ALTER TABLE documents ADD COLUMN user_id INTEGER")

conn.commit()
conn.close()

print("Database upgraded!")