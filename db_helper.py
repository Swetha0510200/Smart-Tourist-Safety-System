###############################################################
# db_helper.py
#
# Tourist Safety Monitoring System
# Database Helper
###############################################################

import sqlite3

DATABASE = "tourist_safety.db"


###############################################################
# Database Connection
###############################################################

def get_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


###############################################################
# Get District Details
###############################################################

def get_area_details(district):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM tourist_safety
        WHERE LOWER(district)=LOWER(?)
        LIMIT 1
    """, (district,))

    row = cursor.fetchone()

    conn.close()

    return row


###############################################################
# Search District
###############################################################

def search_location(district):
    return get_area_details(district)


###############################################################
# Get All Districts
###############################################################

def get_all_districts():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT district
        FROM tourist_safety
        ORDER BY district
    """)

    rows = cursor.fetchall()

    conn.close()

    return rows


###############################################################
# Check Database
###############################################################

def total_districts():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM tourist_safety
    """)

    count = cursor.fetchone()[0]

    conn.close()

    return count


###############################################################
# View Complete Database
###############################################################

def view_database():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM tourist_safety
        ORDER BY district
    """)

    rows = cursor.fetchall()

    conn.close()

    return rows