import sqlite3
import random
import csv

DATABASE_NAME = "tourist_safety.db"
CSV_NAME = "tourist_safety_500.csv"

# -----------------------------------------
# Tamil Nadu Tourist Locations
# -----------------------------------------

tourist_places = {

    "Chennai":[
        ("Marina Beach",13.0500,80.2824),
        ("Elliot Beach",13.0003,80.2667),
        ("Fort St George",13.0827,80.2870),
        ("Kapaleeshwar Temple",13.0339,80.2690),
        ("Government Museum",13.0722,80.2640),
        ("VGP Golden Beach",12.9124,80.2517),
        ("Guindy National Park",13.0108,80.2295),
        ("Anna Nagar Tower Park",13.0850,80.2101)
    ],

    "Coimbatore":[
        ("VOC Park",11.0032,76.9725),
        ("Marudhamalai Temple",11.0453,76.8620),
        ("Isha Yoga Center",10.9862,76.7356),
        ("Siruvani Falls",10.9470,76.6910),
        ("Brookefields Mall",11.0183,76.9725),
        ("Perur Temple",10.9760,76.9123),
        ("Black Thunder",11.3122,76.9415),
        ("Kovai Kutralam",10.9414,76.7602)
    ],

    "Madurai":[
        ("Meenakshi Temple",9.9195,78.1193),
        ("Thirumalai Nayakkar Mahal",9.9160,78.1213),
        ("Alagar Kovil",10.0203,78.1745),
        ("Vaigai Dam",9.8264,77.4947),
        ("Gandhi Museum",9.9340,78.1306),
        ("Samanar Hills",9.8883,78.0675),
        ("Pazhamudhircholai",10.0321,78.1776),
        ("Vandiyur Mariamman Temple",9.9304,78.1502)
    ],

    "Salem":[
        ("Yercaud Lake",11.7753,78.2095),
        ("Pagoda Point",11.7835,78.2145),
        ("Anna Park",11.7741,78.2090),
        ("Kiliyur Falls",11.7793,78.2140),
        ("1008 Lingam Temple",11.6643,78.1460),
        ("Mettur Dam",11.8005,77.8002),
        ("Sugavaneswarar Temple",11.6643,78.1460),
        ("Kurumbapatti Zoo",11.6870,78.1502)
    ],

    "Namakkal":[
        ("Namakkal Fort",11.2194,78.1676),
        ("Anjaneyar Temple",11.2190,78.1675),
        ("Kolli Hills",11.2485,78.3435),
        ("Aagaya Gangai Falls",11.2735,78.3335),
        ("Rasipuram Temple",11.4605,78.1865),
        ("Mohanur River",11.0605,78.1400),
        ("Paramathi Velur",11.1098,78.0031),
        ("Naina Malai",11.3170,78.2050)
    ],

    "Karur":[
        ("Pasupatheswarar Temple",10.9601,78.0766),
        ("Pugalur",10.9301,78.0360),
        ("Kalyana Venkataramana Temple",10.9595,78.0764),
        ("Nerur Temple",10.9032,78.0625),
        ("Amaravathi River",10.9654,78.0863),
        ("Thanthonimalai",10.9607,78.0805),
        ("Karur Bus Stand",10.9600,78.0760),
        ("Textile Market",10.9584,78.0748)
    ],

    "Tiruchirappalli":[
        ("Rock Fort",10.8316,78.6936),
        ("Srirangam Temple",10.8625,78.6932),
        ("Kallanai Dam",10.8525,78.9130),
        ("Samayapuram Temple",10.9305,78.7360),
        ("Butterfly Park",10.8205,78.6905),
        ("Mukkombu",10.9065,78.6034),
        ("St Joseph Church",10.8240,78.6901),
        ("Central Bus Stand",10.7905,78.6804)
    ],

    "Thanjavur":[
        ("Brihadeeswarar Temple",10.7828,79.1318),
        ("Saraswathi Mahal",10.7830,79.1320),
        ("Thanjavur Palace",10.7825,79.1322),
        ("Sivaganga Park",10.7823,79.1335),
        ("Punnainallur Temple",10.8293,79.1744),
        ("Grand Anicut Canal",10.7911,79.1605),
        ("Royal Museum",10.7829,79.1315),
        ("Railway Junction",10.7860,79.1390)
    ],

    "Kanniyakumari":[
        ("Vivekananda Rock",8.0780,77.5550),
        ("Thiruvalluvar Statue",8.0785,77.5546),
        ("Sunrise Point",8.0795,77.5548),
        ("Sunset Point",8.0756,77.5490),
        ("Kanyakumari Beach",8.0790,77.5545),
        ("Padmanabhapuram Palace",8.2505,77.3255),
        ("Mathur Aqueduct",8.3070,77.3150),
        ("Vattakottai Fort",8.1262,77.5660)
    ],

    "Nilgiris":[
        ("Ooty Lake",11.4064,76.6932),
        ("Botanical Garden",11.4125,76.7115),
        ("Doddabetta Peak",11.4065,76.7350),
        ("Pykara Falls",11.4702,76.6045),
        ("Avalanche Lake",11.3020,76.6330),
        ("Emerald Lake",11.3382,76.6155),
        ("Tea Museum",11.4122,76.7055),
        ("Rose Garden",11.4152,76.7065)
    ]
}

# -----------------------------------------
# Database Creation
# -----------------------------------------

conn = sqlite3.connect(DATABASE_NAME)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS tourist_safety(

id INTEGER PRIMARY KEY AUTOINCREMENT,

district TEXT,

location_name TEXT,

latitude REAL,

longitude REAL,

crime_rate TEXT,

crowd_density TEXT,

street_lighting TEXT,

police_distance_km REAL,

hospital_distance_km REAL,

weather TEXT,

road_condition TEXT,

night_travel TEXT,

previous_incidents INTEGER,

geo_fence TEXT,

response_time_min INTEGER,

risk_level TEXT,

safety_score INTEGER

)
""")

conn.commit()

print("Database Created Successfully")
print("Total Districts :", len(tourist_places))

# -----------------------------------------
# Random Data Pools
# -----------------------------------------

crime_levels = ["Low", "Medium", "High"]

crowd_levels = ["Low", "Medium", "High"]

lighting_levels = ["Good", "Average", "Poor"]

weather_types = [
    "Clear",
    "Cloudy",
    "Rain",
    "Fog"
]

road_conditions = [
    "Good",
    "Average",
    "Poor"
]

night_options = [
    "Yes",
    "No"
]

geo_status = [
    "Safe",
    "Outside"
]

# -----------------------------------------
# AI Risk Calculation
# -----------------------------------------

def calculate_risk(
    crime,
    crowd,
    lighting,
    police_distance,
    hospital_distance,
    night,
    incidents,
    geo
):

    score = 100

    # Crime

    if crime == "Medium":
        score -= 15

    elif crime == "High":
        score -= 35

    # Crowd

    if crowd == "Medium":
        score -= 5

    elif crowd == "High":
        score -= 10

    # Street Lighting

    if lighting == "Average":
        score -= 8

    elif lighting == "Poor":
        score -= 18

    # Police Distance

    if police_distance > 2:
        score -= 10

    if police_distance > 5:
        score -= 10

    # Hospital Distance

    if hospital_distance > 3:
        score -= 8

    if hospital_distance > 6:
        score -= 10

    # Night Travel

    if night == "Yes":
        score -= 12

    # Previous Incidents

    score -= incidents * 2

    # Geo Fence

    if geo == "Outside":
        score -= 20

    # Limit

    if score < 0:
        score = 0

    if score > 100:
        score = 100

    # Risk Level

    if score >= 80:
        risk = "Safe"

    elif score >= 60:
        risk = "Medium"

    else:
        risk = "Unsafe"

    return risk, score

# -----------------------------------------
# Record Generator
# -----------------------------------------

generated_records = []

for district in tourist_places:

    locations = tourist_places[district]

    for place in locations:

        name = place[0]
        lat = place[1]
        lon = place[2]

        crime = random.choice(crime_levels)

        crowd = random.choice(crowd_levels)

        lighting = random.choice(lighting_levels)

        police_distance = round(random.uniform(0.5,8),1)

        hospital_distance = round(random.uniform(0.5,10),1)

        weather = random.choice(weather_types)

        road = random.choice(road_conditions)

        night = random.choice(night_options)

        incidents = random.randint(0,8)

        geo = random.choice(geo_status)

        response = random.randint(3,20)

        risk, score = calculate_risk(
            crime,
            crowd,
            lighting,
            police_distance,
            hospital_distance,
            night,
            incidents,
            geo
        )

        generated_records.append(

            (
                district,
                name,
                lat,
                lon,
                crime,
                crowd,
                lighting,
                police_distance,
                hospital_distance,
                weather,
                road,
                night,
                incidents,
                geo,
                response,
                risk,
                score
            )

        )

print("Sample records generated :", len(generated_records))

# -----------------------------------------
# Generate 500 Records
# -----------------------------------------

while len(generated_records) < 500:

    district = random.choice(list(tourist_places.keys()))

    place = random.choice(tourist_places[district])

    name = place[0]
    lat = place[1]
    lon = place[2]

    crime = random.choice(crime_levels)

    crowd = random.choice(crowd_levels)

    lighting = random.choice(lighting_levels)

    police_distance = round(random.uniform(0.5,8),1)

    hospital_distance = round(random.uniform(0.5,10),1)

    weather = random.choice(weather_types)

    road = random.choice(road_conditions)

    night = random.choice(night_options)

    incidents = random.randint(0,8)

    geo = random.choice(geo_status)

    response = random.randint(3,20)

    risk, score = calculate_risk(
        crime,
        crowd,
        lighting,
        police_distance,
        hospital_distance,
        night,
        incidents,
        geo
    )

    generated_records.append(

        (
            district,
            name,
            lat,
            lon,
            crime,
            crowd,
            lighting,
            police_distance,
            hospital_distance,
            weather,
            road,
            night,
            incidents,
            geo,
            response,
            risk,
            score
        )

    )

print("Total Records Generated :", len(generated_records))

# -----------------------------------------
# Insert Into SQLite
# -----------------------------------------

cursor.executemany("""

INSERT INTO tourist_safety(

district,
location_name,
latitude,
longitude,
crime_rate,
crowd_density,
street_lighting,
police_distance_km,
hospital_distance_km,
weather,
road_condition,
night_travel,
previous_incidents,
geo_fence,
response_time_min,
risk_level,
safety_score

)

VALUES(

?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?

)

""", generated_records)

conn.commit()

print("SQLite Database Saved Successfully")

# -----------------------------------------
# Export CSV
# -----------------------------------------

with open(CSV_NAME,"w",newline="",encoding="utf-8") as file:

    writer = csv.writer(file)

    writer.writerow([

        "District",
        "Location Name",
        "Latitude",
        "Longitude",
        "Crime Rate",
        "Crowd Density",
        "Street Lighting",
        "Police Distance(km)",
        "Hospital Distance(km)",
        "Weather",
        "Road Condition",
        "Night Travel",
        "Previous Incidents",
        "Geo Fence",
        "Response Time(min)",
        "Risk Level",
        "Safety Score"

    ])

    writer.writerows(generated_records)

print("CSV File Created Successfully")

# -----------------------------------------
# Close Database
# -----------------------------------------

conn.close()

print("----------------------------------")
print("Dataset Generation Completed")
print("Database :", DATABASE_NAME)
print("CSV :", CSV_NAME)
print("Total Records :", len(generated_records))
print("----------------------------------")