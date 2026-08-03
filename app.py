from flask import Flask, render_template, request, redirect, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from datetime import datetime

import sqlite3
import requests
import os


from safety_predictor import calculate_real_ai

####################################################
# Flask Configuration
####################################################

app = Flask(__name__)

app.secret_key = "tourist_safety_secret"

app.config["UPLOAD_FOLDER"] = "static/uploads"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tourist.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

####################################################
# Create Upload Folder
####################################################

os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

####################################################
# Tourist Safety Database
####################################################

def get_area_details(location):
    conn = sqlite3.connect("tourist_safety.db")
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM tourist_safety
        WHERE district LIKE ?
        LIMIT 1
    """, ("%" + location + "%",))

    row = cursor.fetchone()

    conn.close()

    return row

####################################################
# Database Models
####################################################

class Tourist(db.Model):
    __tablename__ = "tourist"

    id = db.Column(db.Integer, primary_key=True)

    fullname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)

    phone = db.Column(db.String(20))

    emergency_contact1 = db.Column(db.String(20))
    emergency_contact2 = db.Column(db.String(20))
    emergency_contact3 = db.Column(db.String(20))

    password = db.Column(db.String(100), nullable=False)

    dob = db.Column(db.String(30))
    gender = db.Column(db.String(20))
    blood_group = db.Column(db.String(20))
    nationality = db.Column(db.String(50))
    address = db.Column(db.String(250))

    photo = db.Column(db.String(200))

    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)

    location_name = db.Column(db.String(200), default="Location Not Available")

    geo_status = db.Column(db.String(50), default="Unknown")

    travel_status = db.Column(db.String(50), default="Stationary")

    safety_score = db.Column(db.Integer, default=100)

    risk_level = db.Column(db.String(20), default="LOW")


class SafeZone(db.Model):
    __tablename__ = "safe_zone"

    id = db.Column(db.Integer, primary_key=True)

    zone_name = db.Column(db.String(100))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    radius = db.Column(db.Float)


class EmergencyContact(db.Model):
    __tablename__ = "emergency_contact"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100))
    relation = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    priority = db.Column(db.String(30))
    email = db.Column(db.String(100))


class IncidentReport(db.Model):
    __tablename__ = "incident_report"

    id = db.Column(db.Integer, primary_key=True)

    tourist_name = db.Column(db.String(100))
    incident_type = db.Column(db.String(100))
    location = db.Column(db.String(200))
    description = db.Column(db.Text)

    report_time = db.Column(db.String(100))

    severity = db.Column(db.String(30))
    ai_score = db.Column(db.Integer)

    police_required = db.Column(db.String(20))
    medical_required = db.Column(db.String(20))

    response_time = db.Column(db.String(100))

    recommendation = db.Column(db.String(500))


class Admin(db.Model):
    __tablename__ = "admin"

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))

####################################################
# Create Database
####################################################

with app.app_context():

    db.create_all()

    admin = Admin.query.filter_by(username="admin").first()

    if not admin:
        admin = Admin(
            username="admin",
            password="admin123"
        )

        db.session.add(admin)
        db.session.commit()

    zone = SafeZone.query.first()

    if not zone:
        zone = SafeZone(
            zone_name="VSB Engineering College",
            latitude=11.087036,
            longitude=78.096069,
            radius=500
        )

        db.session.add(zone)
        db.session.commit()

        ####################################################
# Home Page
####################################################

@app.route("/")
def home():
    return render_template("login.html", error=None)


####################################################
# Admin Login Page
####################################################

@app.route("/admin")
def admin():
    return render_template("admin_login.html", error=None)


####################################################
# Admin Login
####################################################

@app.route("/admin_login", methods=["POST"])
def admin_login():

    username = request.form.get("username")
    password = request.form.get("password")

    admin = Admin.query.filter_by(
        username=username,
        password=password
    ).first()

    if admin:
        session["admin"] = admin.username
        return redirect("/admin_dashboard")

    return render_template(
        "admin_login.html",
        error="Invalid Admin Login"
    )


####################################################
# User Login
####################################################

@app.route("/login", methods=["POST"])
def login():

    email = request.form.get("email")
    password = request.form.get("password")

    user = Tourist.query.filter_by(
        email=email,
        password=password
    ).first()

    if user:

        session["user"] = user.fullname

        return redirect("/dashboard")

    return render_template(
        "login.html",
        error="❌ Invalid Email or Password"
    )


####################################################
# Register
####################################################

@app.route("/register", methods=["POST"])
def register():

    fullname = request.form.get("fullname")
    email = request.form.get("email")
    phone = request.form.get("phone")

    emergency_contact1 = request.form.get(
        "emergency_contact1", ""
    )

    emergency_contact2 = request.form.get(
        "emergency_contact2", ""
    )

    emergency_contact3 = request.form.get(
        "emergency_contact3", ""
    )

    password = request.form.get("password")

    existing = Tourist.query.filter_by(
        email=email
    ).first()

    if existing:
        return render_template(
            "login.html",
            error="Email already exists"
        )

    tourist = Tourist(

        fullname=fullname,

        email=email,

        phone=phone,

        emergency_contact1=emergency_contact1,

        emergency_contact2=emergency_contact2,

        emergency_contact3=emergency_contact3,

        password=password,

        safety_score=100,

        risk_level="LOW",

        geo_status="Unknown",

        travel_status="Stationary",

        location_name="Location Not Available"

    )

    db.session.add(tourist)
    db.session.commit()

    return redirect("/")


####################################################
# Dashboard
####################################################

@app.route("/dashboard")
def dashboard():

    if "user" not in session:
        return redirect("/")

    user = Tourist.query.filter_by(
        fullname=session["user"]
    ).first()

    if not user:
        session.clear()
        return redirect("/")

    contact_count = 0

    if user.emergency_contact1:
        contact_count += 1

    if user.emergency_contact2:
        contact_count += 1

    if user.emergency_contact3:
        contact_count += 1

    current_location = (
        user.location_name
        if user.location_name
        else "Location Not Available"
    )

    geo_status = (
        user.geo_status
        if user.geo_status
        else "Unknown"
    )

    score = (
        user.safety_score
        if user.safety_score is not None
        else 100
    )

    risk = (
        user.risk_level
        if user.risk_level
        else "LOW"
    )

    status = "SAFE"

    if risk == "HIGH":
        status = "DANGER"

    elif risk == "MEDIUM":
        status = "WARNING"

    return render_template(

        "dashboard.html",

        username=user.fullname,

        current_location=current_location,

        geo_status=geo_status,

        risk=risk,

        safety_score=score,

        status=status,

        contact_count=contact_count,

        contact1=user.emergency_contact1,

        contact2=user.emergency_contact2,

        contact3=user.emergency_contact3

    )

####################################################
# Digital ID
####################################################

@app.route("/digital_id", methods=["GET", "POST"])
def digital_id():

    if "user" not in session:
        return redirect("/")

    tourist = Tourist.query.filter_by(
        fullname=session["user"]
    ).first()

    if request.method == "POST":

        tourist.dob = request.form.get("dob")
        tourist.gender = request.form.get("gender")
        tourist.blood_group = request.form.get("blood_group")
        tourist.nationality = request.form.get("nationality")
        tourist.address = request.form.get("address")

        if "photo" in request.files:

            file = request.files["photo"]

            if file.filename != "":

                filename = secure_filename(file.filename)

                file.save(
                    os.path.join(
                        app.config["UPLOAD_FOLDER"],
                        filename
                    )
                )

                tourist.photo = filename

        db.session.commit()

        return redirect("/digital_id")

    return render_template(
        "digital_id.html",
        tourist=tourist
    )


####################################################
# Edit Profile
####################################################

@app.route("/edit_profile", methods=["GET","POST"])
def edit_profile():

    if "user" not in session:
        return redirect("/")

    tourist = Tourist.query.filter_by(
        fullname=session["user"]
    ).first()

    if request.method=="POST":

        tourist.dob=request.form.get("dob")
        tourist.gender=request.form.get("gender")
        tourist.blood_group=request.form.get("blood_group")
        tourist.nationality=request.form.get("nationality")
        tourist.address=request.form.get("address")

        if "photo" in request.files:

            file=request.files["photo"]

            if file.filename!="":

                filename=secure_filename(file.filename)

                file.save(
                    os.path.join(
                        app.config["UPLOAD_FOLDER"],
                        filename
                    )
                )

                tourist.photo=filename

        db.session.commit()

        return redirect("/digital_id")

    return render_template(
        "edit_profile.html",
        tourist=tourist
    )


####################################################
# Update GPS Location
####################################################

@app.route("/update_location",methods=["POST"])
def update_location():

    if "user" not in session:
        return jsonify({"status":"failed"})

    tourist=Tourist.query.filter_by(
        fullname=session["user"]
    ).first()

    latitude=float(request.form["latitude"])
    longitude=float(request.form["longitude"])

    old_lat=tourist.latitude
    old_lon=tourist.longitude

    tourist.latitude=latitude
    tourist.longitude=longitude


    ####################################################
    # Travel Status
    ####################################################

    if old_lat is None:

        tourist.travel_status="Stationary"

    else:

        movement=((latitude-old_lat)**2+(longitude-old_lon)**2)**0.5

        if movement>0.0001:
            tourist.travel_status="Travelling"
        else:
            tourist.travel_status="Stationary"


    ####################################################
    # Reverse Geocoding
    ####################################################

    try:

        response=requests.get(

            f"https://nominatim.openstreetmap.org/reverse?format=json&lat={latitude}&lon={longitude}",

            headers={
                "User-Agent":"TouristSafetySystem"
            },

            timeout=5

        )

        data=response.json()

        location=data.get(
            "display_name",
            f"{latitude},{longitude}"
        )

    except:

        location=f"{latitude},{longitude}"
    
    
    ####################################################
    # District Detection
    ####################################################

    district="Namakkal"

    districts=[

        "Chennai","Coimbatore","Madurai","Salem","Erode",

        "Namakkal","Karur","Trichy","Tirunelveli",

        "Thoothukudi","Kanyakumari","Thanjavur",

        "Cuddalore","Dharmapuri","Krishnagiri",

        "Tiruppur","Dindigul","Sivagangai",

        "Virudhunagar","Nilgiris","Ramanathapuram"

    ]

    for d in districts:

        if d.lower() in location.lower():

            district=d
            break

    print("Detected District :", district)
    print("Location :", location)


    ####################################################
    # Safety Database Lookup
    ####################################################

    area=get_area_details(district)
    print(area)

    if area:

        tourist.geo_status=area["geo_status"]
        tourist.safety_score=area["safety_score"]
        tourist.risk_level=area["risk_level"]

    else:

        tourist.geo_status="Unknown"
        tourist.safety_score=75
        tourist.risk_level="MEDIUM"

    tourist.location_name=location

    db.session.commit()


    ####################################################
    # Emergency Contact Count
    ####################################################

    contacts=0

    if tourist.emergency_contact1:
        contacts+=1

    if tourist.emergency_contact2:
        contacts+=1

    if tourist.emergency_contact3:
        contacts+=1


    ####################################################
    # Overall Status
    ####################################################

    status="SAFE"

    if tourist.risk_level=="HIGH":
        status="DANGER"

    elif tourist.risk_level=="MEDIUM":
        status="WARNING"


    ####################################################
    # Return JSON
    ####################################################

    return jsonify({

        "current_location":tourist.location_name,

        "geo_status":tourist.geo_status,

        "risk":tourist.risk_level,

        "score":tourist.safety_score,

        "travel_status":tourist.travel_status,

        "contact_count":contacts,

        "status":status

    })

####################################################
# Emergency Contacts
####################################################

@app.route("/emergency_contacts")
def emergency_contacts():

    if "user" not in session:
        return redirect("/")

    contacts = EmergencyContact.query.order_by(
        EmergencyContact.priority
    ).all()

    return render_template(
        "emergency_contacts.html",
        contacts=contacts
    )


####################################################
# Add Contact
####################################################

@app.route("/add_contact", methods=["POST"])
def add_contact():

    if "user" not in session:
        return redirect("/")

    contact = EmergencyContact(

        name=request.form.get("name"),

        relation=request.form.get("relation"),

        phone=request.form.get("phone"),

        priority=request.form.get(
            "priority",
            "Medium"
        ),

        email=request.form.get(
            "email",
            ""
        )

    )

    db.session.add(contact)
    db.session.commit()

    return redirect("/emergency_contacts")


####################################################
# Edit Contact
####################################################

@app.route("/edit_contact/<int:id>", methods=["GET", "POST"])
def edit_contact(id):

    if "user" not in session:
        return redirect("/")

    contact = EmergencyContact.query.get_or_404(id)

    if request.method == "POST":

        contact.name = request.form.get("name")

        contact.relation = request.form.get("relation")

        contact.phone = request.form.get("phone")

        contact.priority = request.form.get(
            "priority",
            "Medium"
        )

        contact.email = request.form.get(
            "email",
            ""
        )

        db.session.commit()

        return redirect("/emergency_contacts")

    return render_template(
        "edit_contact.html",
        contact=contact
    )


####################################################
# Delete Contact
####################################################

@app.route("/delete_contact/<int:id>")
def delete_contact(id):

    if "user" not in session:
        return redirect("/")

    contact = EmergencyContact.query.get_or_404(id)

    db.session.delete(contact)

    db.session.commit()

    return redirect("/emergency_contacts")


####################################################
# Nearby Services
####################################################

@app.route("/nearby")
def nearby():

    if "user" not in session:
        return redirect("/")

    return render_template("nearby.html")


####################################################
# SOS Page
####################################################

@app.route("/sos")
def sos():

    if "user" not in session:
        return redirect("/")

    tourist = Tourist.query.filter_by(
        fullname=session["user"]
    ).first()

    contact_count = 0

    if tourist.emergency_contact1:
        contact_count += 1

    if tourist.emergency_contact2:
        contact_count += 1

    if tourist.emergency_contact3:
        contact_count += 1

    return render_template(

        "sos.html",

        tourist=tourist,

        contact1=tourist.emergency_contact1,

        contact2=tourist.emergency_contact2,

        contact3=tourist.emergency_contact3,

        contact_count=contact_count

    )
####################################################
# AI Risk Analysis
####################################################
@app.route("/ai_risk")
def ai_risk():

    if "user" not in session:
        return redirect("/")

    user = Tourist.query.filter_by(fullname=session["user"]).first()

    if not user:
        return redirect("/")

    # --------------------------
    # Basic User Information
    # --------------------------
    location_name = user.location_name or "Location Not Available"
    geo_status = user.geo_status or "Unknown"
    travel_status = user.travel_status or "Stationary"

    # --------------------------
    # Emergency Contact Count
    # --------------------------
    contact_count = 0

    if user.emergency_contact1:
        contact_count += 1

    if user.emergency_contact2:
        contact_count += 1

    if user.emergency_contact3:
        contact_count += 1

    # --------------------------
    # Detect District
    # --------------------------
    district = "Namakkal"

    districts = [
        "Chennai","Coimbatore","Madurai","Salem","Erode",
        "Namakkal","Karur","Trichy","Tirunelveli",
        "Thoothukudi","Kanyakumari","Thanjavur",
        "Cuddalore","Dharmapuri","Krishnagiri",
        "Tiruppur","Dindigul","Sivagangai",
        "Virudhunagar","Nilgiris","Ramanathapuram"
    ]

    for d in districts:
        if d.lower() in location_name.lower():
            district = d
            break

    # --------------------------
    # Database Lookup
    # --------------------------
    area = get_area_details(district)

    if area:

        analysis = calculate_real_ai(

            crime_rate=area["crime_rate"],
            lighting_score=area["lighting_score"],
            tourist_density=area["tourist_density"],
            police_distance=area["nearest_police_distance"],
            hospital_distance=area["nearest_hospital_distance"],
            emergency_contacts=contact_count,
            geo_status=area["geo_status"],
            travel_status=travel_status

        )

        score = analysis["safety_score"]
        risk = analysis["risk_level"]

    else:

        analysis = {
            "safety_score": 75,
            "risk_level": "MEDIUM",
            "police_required": "No",
            "medical_required": "No",
            "response_time": "20 Minutes"
        }

        score = analysis["safety_score"]
        risk = analysis["risk_level"]
    # --------------------------
    # GPS Status
    # --------------------------
    gps_status = (
        "Live GPS Connected"
        if user.latitude is not None
        else "Waiting for GPS"
    )

    current_hour = datetime.now().hour

    night_status = (
        "High"
        if current_hour >= 20 or current_hour <= 5
        else "Low"
    )

    # --------------------------
    # AI Alert
    # --------------------------
    if risk == "HIGH":

        recent_alert = "High Risk Area Detected"

        ai_reason = "Tourist is in a dangerous area."

    elif risk == "MEDIUM":

        recent_alert = "Moderate Risk"

        ai_reason = "Travel carefully."

    else:

        recent_alert = "Everything Normal"

        ai_reason = "No immediate threats detected."

    geo_alert = (
        "Unsafe Tourist Area"
        if "Unsafe" in geo_status
        else "Safe Tourist Area"
    )

    geo_alert_description = (
        "AI detected unsafe area."
        if "Unsafe" in geo_status
        else "Current location is safe."
    )

    ai_update = "Live AI Monitoring Active"

    # --------------------------
    # Recommendations
    # --------------------------
    if risk == "HIGH":

        recommendation = [
            "Move to nearest safe zone.",
            "Share live location.",
            "Press SOS.",
            "Avoid travelling alone."
        ]

    elif risk == "MEDIUM":

        recommendation = [
            "Remain alert.",
            "Avoid isolated places.",
            "Keep GPS enabled."
        ]

    else:

        recommendation = [
            "Area appears safe.",
            "Enjoy your trip."
        ]

    return render_template(

        "ai_risk.html",

        user=user,
        area=area,

        risk=risk,
        score=score,

        safety_score=score,
        overall_risk=risk,

        emergency_contacts=contact_count,

        location_name=location_name,
        geo_status=geo_status,
        travel_status=travel_status,

        gps_status=gps_status,
        night_status=night_status,

        recent_alert=recent_alert,
        ai_reason=ai_reason,

        geo_alert=geo_alert,
        geo_alert_description=geo_alert_description,

        ai_update=ai_update,

        recommendation=recommendation,

        contact_count=contact_count,

        latitude=user.latitude,
        longitude=user.longitude,

        police_required=analysis["police_required"],

        medical_required=analysis["medical_required"],

        response_time=analysis["response_time"],

        geo_fence="Inside Safe Zone" if "Safe" in geo_status else "Outside Safe Zone",

        night_travel="Night" if current_hour >= 22 or current_hour <= 5 else "Day"
   
    )

####################################################
# Incident Report
####################################################

@app.route("/incident_report", methods=["GET","POST"])
def incident_report():

    if "user" not in session:
        return redirect("/")

    tourist = Tourist.query.filter_by(
        fullname=session["user"]
    ).first()

    if request.method == "POST":

        location = request.form.get("location")

        area = get_area_details(location)

        contact_count = 0

        if tourist.emergency_contact1:
            contact_count += 1
        if tourist.emergency_contact2:
            contact_count += 1
        if tourist.emergency_contact3:
            contact_count += 1

        if area:

            ai = calculate_real_ai(

                crime_rate=area["crime_rate"],
                lighting_score=area["lighting_score"],
                tourist_density=area["tourist_density"],
                police_distance=area["nearest_police_distance"],
                hospital_distance=area["nearest_hospital_distance"],
                emergency_contacts=contact_count,
                geo_status=area["geo_status"],
                travel_status=tourist.travel_status

            )

        else:

            ai = {

                "risk_level":"MEDIUM",
                "safety_score":75,
                "police_required":"No",
                "medical_required":"No",
                "response_time":"20 Minutes"

            }

        if ai["risk_level"] == "HIGH":

            recommendation = "Move immediately to a safe place and press SOS."

        elif ai["risk_level"] == "MEDIUM":

            recommendation = "Travel carefully. Stay alert."

        else:

            recommendation = "Area appears safe. Continue your journey."

        incident = IncidentReport(

            tourist_name=tourist.fullname,

            incident_type=request.form.get("incident_type"),

            location=location,

            description=request.form.get("description"),

            report_time=datetime.now().strftime("%d-%m-%Y %H:%M"),

            severity=ai["risk_level"],

            ai_score=ai["safety_score"],

            police_required=ai["police_required"],

            medical_required=ai["medical_required"],

            response_time=ai["response_time"],

            recommendation=recommendation

        )

        db.session.add(incident)

        db.session.commit()

        return redirect("/incident_report")

    reports = IncidentReport.query.order_by(
    IncidentReport.id.desc()
    ).all()

# Get district details from database
    district = "Namakkal"

    if tourist.location_name:
        for d in [
            "Chennai","Coimbatore","Madurai","Salem","Erode",
            "Namakkal","Karur","Thanjavur","Trichy",
            "Tirunelveli","Thoothukudi","Kanyakumari"
        ]:
            if d.lower() in tourist.location_name.lower():
                district = d
                break

# AI Analysis
    area =get_area_details(district)
    
    contact_count = 0

    if tourist.emergency_contact1:
        contact_count += 1
    if tourist.emergency_contact2:
        contact_count += 1
    if tourist.emergency_contact3:
        contact_count += 1

    if area:

        analysis = calculate_real_ai(

            crime_rate=area["crime_rate"],
            lighting_score=area["lighting_score"],
            tourist_density=area["tourist_density"],
            police_distance=area["nearest_police_distance"],
            hospital_distance=area["nearest_hospital_distance"],
            emergency_contacts=contact_count,
            geo_status=area["geo_status"],
            travel_status=tourist.travel_status

        )
        analysis["overall_risk"] = analysis["risk_level"]
        analysis["geo_fence"] = area["geo_status"]
        analysis["travel_status"] = tourist.travel_status
        analysis["current_location"] = tourist.location_name

    else:

        analysis = {
            "safety_score": 75,
            "risk_level": "MEDIUM",
            "police_required": "No",
            "medical_required": "No",
            "response_time": "20 Minutes"
        }

        score = analysis["safety_score"]
        risk = analysis["risk_level"]

    current_hour = datetime.now().hour

    if current_hour >= 20 or current_hour <= 5:
        analysis["night_travel"] = "Night"
    else:
        analysis["night_travel"] = "Day"

    if analysis["risk_level"] == "HIGH":
        analysis["recommendation"] = "Move immediately to a safe place and press SOS."
    elif analysis["risk_level"] == "MEDIUM":
        analysis["recommendation"] = "Travel carefully. Stay alert."
    else:
        analysis["recommendation"] = "Area appears safe. Continue your journey."

    analysis["emergency_contacts"] = contact_count
    
    return render_template(
        "incident_report.html",
        tourist=tourist,
        reports=reports,
        tourist_name=tourist.fullname,
        analysis=analysis
    )

####################################################
# Admin Dashboard
####################################################

@app.route("/admin_dashboard")
def admin_dashboard():

    if "admin" not in session:
        return redirect("/admin")

    tourists = Tourist.query.all()

    incidents = IncidentReport.query.order_by(
        IncidentReport.id.desc()
    ).all()

    return render_template(
        "admin_dashboard.html",
        tourists=tourists,
        incidents=incidents,
        total_tourists=Tourist.query.count(),
        total_contacts=EmergencyContact.query.count(),
        total_incidents=IncidentReport.query.count()
    )

####################################################
# Admin Incidents
####################################################

@app.route("/admin_incidents")
def admin_incidents():

    if "admin" not in session:
        return redirect("/admin")

    incidents = IncidentReport.query.order_by(
        IncidentReport.id.desc()
    ).all()

    return render_template(
        "admin_incidents.html",
        incidents=incidents
    )

####################################################
# Admin Tourists
####################################################

@app.route("/admin_tourists")
def admin_tourists():

    if "admin" not in session:
        return redirect("/admin")

    tourists = Tourist.query.all()

    return render_template(
        "admin_tourists.html",
        tourists=tourists
    )

####################################################
# Admin Contacts
####################################################

@app.route("/admin_contacts")
def admin_contacts():

    if "admin" not in session:
        return redirect("/admin")

    contacts = EmergencyContact.query.all()

    return render_template(
        "admin_contacts.html",
        contacts=contacts
    )

####################################################
# Admin GPS
####################################################

@app.route("/admin_gps")
def admin_gps():

    if "admin" not in session:
        return redirect("/admin")

    tourists = Tourist.query.all()

    return render_template(
        "admin_gps.html",
        tourists=tourists
    )

####################################################
# Admin AI Monitor
####################################################

@app.route("/admin_ai_monitor")
def admin_ai_monitor():

    if "admin" not in session:
        return redirect("/admin")

    tourists = Tourist.query.all()

    return render_template(
        "admin_ai_monitor.html",
        tourists=tourists
    )

####################################################
# Analytics
####################################################

@app.route("/admin_analytics")
def admin_analytics():

    if "admin" not in session:
        return redirect("/admin")

    
    low_risk = Tourist.query.filter_by(risk_level="LOW").count()

    medium_risk = Tourist.query.filter_by(risk_level="MEDIUM").count()

    high_risk = Tourist.query.filter_by(risk_level="HIGH").count()

    return render_template(

        "admin_analytics.html",

        total_tourists=Tourist.query.count(),

        total_contacts=EmergencyContact.query.count(),

        total_incidents=IncidentReport.query.count(),

        low_risk=low_risk,
        medium_risk=medium_risk,
        high_risk=high_risk,

        low_count = IncidentReport.query.filter_by(
            severity="Low"
        ).count(),

        medium_count = IncidentReport.query.filter_by(
            severity="Medium"
        ).count(),

        high_count = IncidentReport.query.filter_by(
            severity="High"
        ).count(),

        critical_count = 0
    )

####################################################
# Logout
####################################################

@app.route("/logout")
def logout():

    session.clear()

    return redirect("/")

####################################################
# Run Application
####################################################

if __name__ == "__main__":
    app.run(debug=True)