import sqlite3
import os

# ----------------------------------------
# Remove old database if it exists
# ----------------------------------------

DB_NAME = "tourist_safety.db"

if os.path.exists(DB_NAME):
    os.remove(DB_NAME)
    print("Old database removed.")

# ----------------------------------------
# Create new database
# ----------------------------------------

conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()

# ----------------------------------------
# Create tourist_safety table
# ----------------------------------------

cursor.execute("""
CREATE TABLE tourist_safety (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    district TEXT UNIQUE,

    geo_status TEXT,

    safety_score INTEGER,

    risk_level TEXT,

    crime_rate INTEGER,

    lighting_score INTEGER,

    tourist_density INTEGER,

    nearest_police_distance REAL,

    nearest_hospital_distance REAL,

    police_required TEXT,

    medical_required TEXT,

    response_time TEXT

)
""")

conn.commit()

print("Database created successfully.")
print("Table tourist_safety created successfully.")

conn.close()