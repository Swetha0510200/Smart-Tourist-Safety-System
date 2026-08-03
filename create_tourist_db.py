import sqlite3

conn = sqlite3.connect("tourist_safety.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE tourist_safety (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    district TEXT,
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

cursor.execute("""
INSERT INTO tourist_safety (
district,
geo_status,
safety_score,
risk_level,
crime_rate,
lighting_score,
tourist_density,
nearest_police_distance,
nearest_hospital_distance,
police_required,
medical_required,
response_time
)
VALUES (
'Namakkal',
'Safe Tourist Area',
85,
'LOW',
20,
90,
70,
1.5,
2.0,
'No',
'No',
'5 Minutes'
)
""")

conn.commit()
conn.close()

print("Database created successfully.")