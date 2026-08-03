import sqlite3

conn = sqlite3.connect("tourist_safety.db")


cursor = conn.cursor()

cursor.execute("PRAGMA table_info(tourist_safety)")

columns = cursor.fetchall()

print("\nColumns in tourist_safety table:\n")

for c in columns:
    print(c)

conn.close()