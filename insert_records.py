import sqlite3

conn = sqlite3.connect("tourist_safety.db")
cursor = conn.cursor()


# Delete old table if it exists
cursor.execute("DROP TABLE IF EXISTS tourist_safety")

# Create table
cursor.execute("""
CREATE TABLE tourist_safety(

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

districts = [

(
"Chennai",
"Safe Zone",
90,
"LOW",
18,
95,
98,
0.8,
1.0,
"No",
"No",
"5 Minutes"
),

(
"Coimbatore",
"Safe Zone",
88,
"LOW",
22,
90,
90,
1.2,
1.5,
"No",
"No",
"6 Minutes"
),

(
"Madurai",
"Moderately Safe",
78,
"MEDIUM",
40,
75,
82,
1.5,
2.0,
"No",
"No",
"8 Minutes"
),

(
"Tiruchirappalli",
"Safe Zone",
86,
"LOW",
25,
88,
84,
1.0,
1.4,
"No",
"No",
"6 Minutes"
),

(
"Salem",
"Moderately Safe",
75,
"MEDIUM",
42,
72,
70,
2.0,
2.5,
"No",
"No",
"10 Minutes"
),

(
"Erode",
"Safe Zone",
85,
"LOW",
20,
90,
72,
1.3,
1.7,
"No",
"No",
"7 Minutes"
),

(
"Namakkal",
"Safe Zone",
92,
"LOW",
15,
96,
65,
0.9,
1.2,
"No",
"No",
"5 Minutes"
),

(
"Karur",
"Safe Zone",
89,
"LOW",
17,
94,
60,
0.8,
1.1,
"No",
"No",
"5 Minutes"
),

(
"Dharmapuri",
"Moderately Safe",
72,
"MEDIUM",
48,
70,
55,
2.8,
3.0,
"Yes",
"No",
"12 Minutes"
),

(
"Krishnagiri",
"Moderately Safe",
74,
"MEDIUM",
45,
74,
58,
2.5,
2.8,
"Yes",
"No",
"12 Minutes"
),

(
"Dindigul",
"Moderately Safe",
76,
"MEDIUM",
38,
78,
62,
2.1,
2.4,
"No",
"No",
"10 Minutes"
),

(
"Thanjavur",
"Safe Zone",
87,
"LOW",
21,
91,
70,
1.2,
1.6,
"No",
"No",
"6 Minutes"
),

(
"Nagapattinam",
"Moderately Safe",
73,
"MEDIUM",
43,
76,
55,
2.4,
2.8,
"Yes",
"No",
"11 Minutes"
),

(
"Mayiladuthurai",
"Safe Zone",
83,
"LOW",
24,
86,
57,
1.8,
2.0,
"No",
"No",
"8 Minutes"
),

(
"Cuddalore",
"Moderately Safe",
72,
"MEDIUM",
46,
73,
60,
2.7,
2.9,
"Yes",
"No",
"12 Minutes"
),

(
"Villupuram",
"Moderately Safe",
71,
"MEDIUM",
47,
72,
54,
2.9,
3.1,
"Yes",
"No",
"13 Minutes"
),

(
"Kallakurichi",
"Moderately Safe",
70,
"MEDIUM",
49,
71,
50,
3.0,
3.2,
"Yes",
"No",
"13 Minutes"
),

(
"Tiruvannamalai",
"Moderately Safe",
74,
"MEDIUM",
41,
77,
59,
2.3,
2.5,
"No",
"No",
"10 Minutes"
),

(
"Vellore",
"Safe Zone",
82,
"LOW",
28,
85,
72,
1.7,
1.9,
"No",
"No",
"8 Minutes"
),

(
"Ranipet",
"Safe Zone",
84,
"LOW",
26,
87,
66,
1.5,
1.8,
"No",
"No",
"7 Minutes"
),

(
"Tirupattur",
"Moderately Safe",
73,
"MEDIUM",
44,
75,
54,
2.5,
2.8,
"Yes",
"No",
"11 Minutes"
),

(
"Kancheepuram",
"Safe Zone",
86,
"LOW",
22,
90,
80,
1.3,
1.6,
"No",
"No",
"6 Minutes"
),

(
"Chengalpattu",
"Safe Zone",
85,
"LOW",
23,
89,
78,
1.4,
1.7,
"No",
"No",
"6 Minutes"
),

(
"Tiruvallur",
"Moderately Safe",
77,
"MEDIUM",
37,
79,
74,
2.0,
2.2,
"No",
"No",
"9 Minutes"
),

(
"Sivagangai",
"Moderately Safe",
74,
"MEDIUM",
42,
76,
58,
2.3,
2.6,
"No",
"No",
"10 Minutes"
),

(
"Ramanathapuram",
"Moderately Safe",
72,
"MEDIUM",
45,
72,
60,
2.7,
3.0,
"Yes",
"No",
"12 Minutes"
),

(
"Virudhunagar",
"Safe Zone",
81,
"LOW",
30,
84,
68,
1.8,
2.0,
"No",
"No",
"8 Minutes"
),

(
"Thoothukudi",
"Safe Zone",
83,
"LOW",
28,
86,
72,
1.7,
1.9,
"No",
"No",
"8 Minutes"
),

(
"Tirunelveli",
"Safe Zone",
85,
"LOW",
24,
88,
75,
1.4,
1.7,
"No",
"No",
"7 Minutes"
),

(
"Tenkasi",
"Safe Zone",
82,
"LOW",
27,
85,
64,
1.8,
2.0,
"No",
"No",
"8 Minutes"
),

(
"Kanyakumari",
"Safe Zone",
90,
"LOW",
18,
94,
82,
1.0,
1.3,
"No",
"No",
"5 Minutes"
),

(
"The Nilgiris",
"Safe Zone",
91,
"LOW",
15,
96,
76,
1.1,
1.4,
"No",
"No",
"5 Minutes"
),

(
"Tiruppur",
"Moderately Safe",
79,
"MEDIUM",
34,
82,
69,
1.9,
2.2,
"No",
"No",
"9 Minutes"
),

(
"Ariyalur",
"Safe Zone",
84,
"LOW",
25,
88,
60,
1.6,
1.9,
"No",
"No",
"7 Minutes"
),

(
"Perambalur",
"Safe Zone",
83,
"LOW",
26,
87,
59,
1.7,
2.0,
"No",
"No",
"7 Minutes"
),

(
"Pudukkottai",
"Safe Zone",
82,
"LOW",
28,
85,
61,
1.8,
2.0,
"No",
"No",
"8 Minutes"
),

(
"Theni",
"Safe Zone",
84,
"LOW",
24,
88,
58,
1.5,
1.8,
"No",
"No",
"7 Minutes"
),

(
"Tiruvarur",
"Moderately Safe",
76,
"MEDIUM",
39,
80,
55,
2.2,
2.5,
"No",
"No",
"10 Minutes"
)

]

cursor.executemany("""
INSERT INTO tourist_safety(
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
VALUES(?,?,?,?,?,?,?,?,?,?,?,?)
""", districts)

conn.commit()

print("=" * 60)
print("All 38 Tamil Nadu districts inserted successfully.")
print("Database : tourist_safety.db")
print("Table    : tourist_safety")
print("=" * 60)

conn.close()