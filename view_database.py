import sqlite3

DATABASE = "tourist_safety.db"

try:
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type='table'
    """)

    tables = cursor.fetchall()

    print("\nTables Found:\n")

    for table in tables:

        print(table[0])

        cursor.execute(f"SELECT * FROM {table[0]} LIMIT 5")

        rows = cursor.fetchall()

        for row in rows:
            print(row)

        print("-" * 50)

    conn.close()

except Exception as e:

    print("\nError:")
    print(e)