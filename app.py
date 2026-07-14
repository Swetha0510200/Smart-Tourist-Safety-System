from flask import Flask, render_template, request, redirect, session, jsonify



from flask_sqlalchemy import SQLAlchemy



from werkzeug.utils import secure_filename



from datetime import datetime



import requests

import os

# ----------------------------------------
# AREA RISK DATABASE
# ----------------------------------------

AREA_DATABASE = {

    "Mohanur": "SAFE",
    "Namakkal": "SAFE",
    "Karur": "SAFE",
    "Salem": "SAFE",
    "VSB Engineering College": "SAFE",

    "Forest": "HIGH",
    "Reserve Forest": "HIGH",
    "Highway": "HIGH"

}


app = Flask(__name__)

app.secret_key = "tourist_safety_secret"

app.config["UPLOAD_FOLDER"] = "static/uploads"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tourist.db"

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# Create upload folder automatically



if not os.path.exists(app.config["UPLOAD_FOLDER"]):



    os.makedirs(app.config["UPLOAD_FOLDER"])



# ====================================================

# Tourist Table

# ====================================================
class Tourist(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    fullname = db.Column(db.String(100))





    email = db.Column(db.String(100), unique=True)





    phone = db.Column(db.String(20))





    emergency_contact1 = db.Column(db.String(20))





    emergency_contact2 = db.Column(db.String(20))





    emergency_contact3 = db.Column(db.String(20))





    password = db.Column(db.String(100))





    dob = db.Column(db.String(30))





    gender = db.Column(db.String(20))





    blood_group = db.Column(db.String(20))





    nationality = db.Column(db.String(50))





    address = db.Column(db.String(250))





    photo = db.Column(db.String(200))

    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    location_name = db.Column(

        db.String(200),

        default="Location Not Available"

    )

    geo_status = db.Column(

        db.String(50),

        default="Unknown"

    )





    travel_status = db.Column(

        db.String(50),

        default="Unknown"

    )





    safety_score = db.Column(

        db.Integer,

        default=100

    )





    risk_level = db.Column(

        db.String(20),

        default="LOW"

    )

# ====================================================

# Safe Zone Table

# ====================================================


class SafeZone(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    zone_name = db.Column(db.String(100))

    latitude = db.Column(db.Float)

    longitude = db.Column(db.Float)

    radius = db.Column(db.Float)

# ====================================================

# Emergency Contact Table

# ====================================================

class EmergencyContact(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100))

    relation = db.Column(db.String(100))

    phone = db.Column(db.String(20))

    priority = db.Column(db.String(30))

    email = db.Column(db.String(100))

# ====================================================

# Incident Report Table

# ====================================================

class IncidentReport(db.Model):

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
# ====================================================

# Admin Table

# ====================================================

class Admin(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(100))

    password = db.Column(db.String(100))

    # ====================================================

# CREATE DATABASE

# ====================================================

with app.app_context():

    db.create_all()

    admin = Admin.query.filter_by(

        username="admin"

    ).first()

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

# ====================================================

# ADMIN LOGIN PAGE

# ====================================================





@app.route("/admin")

def admin():



    return render_template(

        "admin_login.html",

        error=None

    )











# ====================================================

# ADMIN LOGIN

# ====================================================





@app.route("/admin_login", methods=["POST"])

def admin_login():





    username = request.form["username"]

    password = request.form["password"]

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

# ====================================================

# HOME PAGE

# ====================================================





@app.route("/")

def home():

    return render_template(



        "login.html",



        error=None



    )

# ====================================================

# USER LOGIN

# ====================================================





@app.route("/login", methods=["POST"])

def login():





    email = request.form["email"]





    password = request.form["password"]







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

# ====================================================

# REGISTER

# ====================================================





@app.route("/register", methods=["POST"])

def register():

    fullname = request.form["fullname"]
    email = request.form["email"]
    phone = request.form["phone"]

    emergency_contact1 = request.form.get(

        "emergency_contact1",

        ""

    )





    emergency_contact2 = request.form.get(

        "emergency_contact2",

        ""

    )





    emergency_contact3 = request.form.get(

        "emergency_contact3",

        ""

    )





    password = request.form["password"]







    existing = Tourist.query.filter_by(

        email=email

    ).first()







    if existing:





        return "Email already exists"







    tourist = Tourist(



        fullname=fullname,



        email=email,



        phone=phone,



        emergency_contact1=emergency_contact1,



        emergency_contact2=emergency_contact2,



        emergency_contact3=emergency_contact3,



        password=password



    )







    db.session.add(tourist)





    db.session.commit()







    return redirect("/")











# ====================================================

# DASHBOARD

# ====================================================





@app.route("/dashboard")

def dashboard():





    if "user" not in session:



        return redirect("/")







    user = Tourist.query.filter_by(



        fullname=session["user"]



    ).first()







    contact_count = 0



    if user.emergency_contact1 and user.emergency_contact1.strip():

        contact_count += 1



    if user.emergency_contact2 and user.emergency_contact2.strip():

        contact_count += 1



    if user.emergency_contact3 and user.emergency_contact3.strip():

        contact_count += 1







    current_location = user.location_name





    if not current_location:



        current_location = "Location Not Available"







    geo_status = user.geo_status







    if not geo_status:



        geo_status="Unknown"







    score = user.safety_score







    if score is None:



        score=100







    risk = user.risk_level







    if not risk:



        risk="LOW"







    status="SAFE"







    if risk=="HIGH":



        status="DANGER"





    elif risk=="MEDIUM":



        status="WARNING"


    return render_template(



        "dashboard.html",



        username=user.fullname,



        current_location=current_location,



        geo_status=geo_status,



        risk=risk,



        safety_score=score,



        contact_count=contact_count,



        contact1=user.emergency_contact1,



        contact2=user.emergency_contact2,



        contact3=user.emergency_contact3,



        status=status



    )



# ====================================================

# DIGITAL ID

# ====================================================





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

            if file.filename:

                filename = secure_filename(

                    file.filename

                )





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

# ====================================================

# EDIT PROFILE

# ====================================================





@app.route("/edit_profile", methods=["GET","POST"])

def edit_profile():


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


            if file.filename:

                filename = secure_filename(

                    file.filename

                )

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



        "edit_profile.html",



        tourist=tourist



    )
# ====================================================

# UPDATE GPS LOCATION

# ====================================================
# ====================================================
# UPDATE GPS LOCATION
# ====================================================

@app.route("/update_location", methods=["POST"])
def update_location():

    if "user" not in session:
        return jsonify({"status": "failed"})

    tourist = Tourist.query.filter_by(
        fullname=session["user"]
    ).first()

    latitude = float(request.form["latitude"])
    longitude = float(request.form["longitude"])

    old_lat = tourist.latitude
    old_lon = tourist.longitude

    tourist.latitude = latitude
    tourist.longitude = longitude

    # ----------------------------
    # Travel Status
    # ----------------------------

    if old_lat is None or old_lon is None:
        tourist.travel_status = "Stationary"

    else:
        movement = (((latitude - old_lat) ** 2) +
                    ((longitude - old_lon) ** 2)) ** 0.5

        if movement > 0.0001:
            tourist.travel_status = "Travelling"
        else:
            tourist.travel_status = "Stationary"

    # ----------------------------
    # Get Current Location
    # ----------------------------

    try:
        response = requests.get(
            f"https://nominatim.openstreetmap.org/reverse?format=json&lat={latitude}&lon={longitude}",
            headers={"User-Agent": "TouristSafetySystem"},
            timeout=5
        )

        data = response.json()

        location = data.get(
            "display_name",
            f"{latitude},{longitude}"
        )

    except:
        location = f"{latitude},{longitude}"

    # ----------------------------
    # Area Classification
    # ----------------------------

    location_lower = location.lower()

    safe_places = [
        "vsb engineering college",
        "college",
        "school",
        "hospital",
        "police",
        "police station",
        "bus stand",
        "railway station",
        "airport",
        "temple",
        "mall",
        "market",
        "city",
        "town",
        "mohanur",
        "namakkal",
        "karur",
        "salem"
    ]

    unsafe_places = [
        "forest",
        "reserve forest",
        "mountain",
        "highway",
        "river",
        "lake",
        "desert",
        "isolated",
        "remote"
    ]

    if any(place in location_lower for place in safe_places):
        geo_status = "🟢 Safe Tourist Area"

    elif any(place in location_lower for place in unsafe_places):
        geo_status = "🔴 Unsafe Tourist Area"

    else:
        geo_status = "🟡 Moderate Risk Area"

    # ----------------------------
    # Emergency Contacts
    # ----------------------------

    contacts = 0

    if tourist.emergency_contact1:
        contacts += 1

    if tourist.emergency_contact2:
        contacts += 1

    if tourist.emergency_contact3:
        contacts += 1

    # ----------------------------
    # Safety Score
    # ----------------------------

    score = 100

    # Area Risk

    if geo_status == "🟢 Safe Tourist Area":
        score -= 0

    elif geo_status == "🟡 Moderate Risk Area":
        score -= 20

    else:
        score -= 40

    # Emergency Contacts

    if contacts == 0:
        score -= 40

    elif contacts == 1:
        score -= 20

    elif contacts == 2:
        score -= 10

    # Night Travel

    hour = datetime.now().hour

    if hour >= 22 or hour <= 5:
        score -= 15

    # ----------------------------
    # Final Risk
    # ----------------------------

    if score >= 85:
        risk = "🟢 LOW"
        status = "SAFE"

    elif score >= 60:
        risk = "🟡 MEDIUM"
        status = "CAUTION"

    else:
        risk = "🔴 HIGH"
        status = "DANGER"

    # ----------------------------
    # Save
    # ----------------------------

    tourist.location_name = location
    tourist.geo_status = geo_status
    tourist.safety_score = score
    tourist.risk_level = risk

    db.session.commit()

    return jsonify({
        "current_location": location,
        "geo_status": geo_status,
        "risk": risk,
        "contact_count": contacts,
        "status": status,
        "travel_status": tourist.travel_status
    })

# ====================================================

# EMERGENCY CONTACTS

# ====================================================

@app.route("/emergency_contacts")

def emergency_contacts():

    if "user" not in session:

        return redirect("/")

    contacts = EmergencyContact.query.all()

    return render_template(

        "emergency_contacts.html",
        contacts=contacts

    )

@app.route("/add_contact", methods=["POST"])

def add_contact():

    contact = EmergencyContact(
        name=request.form["name"],
        relation=request.form["relation"],
        phone=request.form["phone"],
        priority=request.form.get(

            "priority",

            ""

        ),

        email=request.form.get(

            "email",

            ""

        )
    )
    db.session.add(contact)
    db.session.commit()

    return redirect("/emergency_contacts")

@app.route("/edit_contact/<int:id>", methods=["GET","POST"])

def edit_contact(id):

    contact = EmergencyContact.query.get_or_404(id)

    if request.method=="POST":

        contact.name=request.form["name"]

        contact.phone=request.form["phone"]

        contact.relation=request.form["relation"]

        contact.priority=request.form.get(

            "priority",

            ""

        )

        contact.email=request.form.get(

            "email",

            ""

        )

        db.session.commit()

        return redirect("/emergency_contacts")

    return render_template(

        "edit_contact.html",

        contact=contact

    )

@app.route("/delete_contact/<int:id>")

def delete_contact(id):

    contact=EmergencyContact.query.get_or_404(id)
    db.session.delete(contact)

    db.session.commit()

    return redirect("/emergency_contacts")

# ====================================================

# AI RISK ANALYSIS

# ====================================================

@app.route("/ai_risk")

def ai_risk():



    if "user" not in session:

        return redirect("/")



    user = Tourist.query.filter_by(

        fullname=session["user"]

    ).first()



    # ----------------------------

    # Basic Information

    # ----------------------------



    score = user.safety_score if user.safety_score else 100



    risk = user.risk_level.replace("🟢 ","").replace("🟡 ","").replace("🔴 ","") if user.risk_level else "LOW"



    geo_status = user.geo_status if user.geo_status else "Unknown"



    location_name = user.location_name if user.location_name else "Location Not Available"



    travel_status = user.travel_status if user.travel_status else "Stationary"



    # ----------------------------

    # Contact Count

    # ----------------------------

    contact_count = 0

    if user.emergency_contact1 and user.emergency_contact1.strip():

        contact_count += 1

    if user.emergency_contact2 and user.emergency_contact2.strip():

        contact_count += 1



    if user.emergency_contact3 and user.emergency_contact3.strip():

        contact_count += 1

    # ----------------------------

    # GPS Status

    # ----------------------------



    if user.latitude and user.longitude:

        gps_status = "Live GPS Connected"

    else:

        gps_status = "Waiting for GPS"


    # ----------------------------

    # Night Travel

    # ----------------------------



    current_hour = datetime.now().hour



    if current_hour >= 22 or current_hour <= 5:

        night_status = "High"

    else:

        night_status = "Low"



    # ----------------------------

    # Recent Alert

    # ----------------------------



    if risk == "HIGH":

        recent_alert = "High Risk Area Detected"

        ai_reason = "Tourist is outside the safe zone with low safety score."



    elif risk == "MEDIUM":

        recent_alert = "Moderate Risk"

        ai_reason = "Travel carefully and avoid isolated places."



    else:

        recent_alert = "Everything Normal"

        ai_reason = "No immediate threats detected."



    # ----------------------------

    # Geo Alert

    # ----------------------------



    if "Unsafe" in geo_status:

        geo_alert = "Unsafe Tourist Area"
        geo_alert_description = "AI detected that your current location is classified as an unsafe tourist area."

    else:
        geo_alert = "Safe Tourist Area"
        geo_alert_description = "Your current location is classified as a safe tourist area."


    # ----------------------------

    # AI Update

    # ----------------------------



    ai_update = "Live AI Monitoring Active"



    # ----------------------------

    # Recommendation

    # ----------------------------



    if risk == "HIGH":



        recommendation = [

            "Move immediately to the nearest safe zone.",

            "Share your live location with family.",

            "Use the SOS button if you feel unsafe.",

            "Avoid travelling alone.",

            "Contact nearby police if required."

        ]



    elif risk == "MEDIUM":



        recommendation = [

            "Remain alert.",

            "Avoid isolated places.",

            "Keep GPS enabled.",

            "Stay connected with emergency contacts.",

            "Monitor AI alerts."

        ]



    else:



        recommendation = [

            "Area appears safe.",

            "Continue your journey.",

            "Keep location services enabled.",

            "Update digital identity regularly.",

            "Enjoy your trip safely."

        ]



    response_time = "5 - 10 Minutes"

    safety_score = score

    

    latitude = user.latitude if user.latitude is not None else "Not Available"

    longitude = user.longitude if user.longitude is not None else "Not Available"



    police_required = "Required" if risk == "HIGH" else "Not Required"



    medical_required = "Required" if risk == "HIGH" else "Not Required"



    return render_template(

    "ai_risk.html",



    risk=risk,

    score=score,

    location_name=location_name,

    contact_count=contact_count,


    geo_status=geo_status,

    travel_status=travel_status,
    night_status=night_status,

    recommendation=recommendation,
    gps_status=gps_status,
    recent_alert=recent_alert,



    ai_reason=ai_reason,

    geo_alert=geo_alert,

    geo_alert_description=geo_alert_description,
    ai_update=ai_update,
    latitude=latitude,
    longitude=longitude,
    geo_fence="Inside Safe Zone" if "Safe Tourist Area" in geo_status else "Outside Safe Zone",
    night_travel="Night" if current_hour >= 22 or current_hour <= 5 else "Day",
    emergency_contacts=contact_count,
    safety_score=score,
    overall_risk=risk,
    response_time=response_time,
    police_required=police_required,
    medical_required=medical_required

)

# ====================================================

# NEARBY SERVICES

# ====================================================

@app.route("/nearby")

def nearby():
    if "user" not in session:



        return redirect("/")







    return render_template(

        "nearby.html"

    )











# ====================================================

# SOS PAGE

# ====================================================





@app.route("/sos")

def sos():





    if "user" not in session:



        return redirect("/")







    tourist=Tourist.query.filter_by(



        fullname=session["user"]



    ).first()







    contact_count = 0



    if tourist.emergency_contact1 and tourist.emergency_contact1.strip():

        contact_count += 1



    if tourist.emergency_contact2 and tourist.emergency_contact2.strip():

        contact_count += 1



    if tourist.emergency_contact3 and tourist.emergency_contact3.strip():

        contact_count += 1









    return render_template(



        "sos.html",



        tourist=tourist,



        contact1=tourist.emergency_contact1,



        contact2=tourist.emergency_contact2,



        contact3=tourist.emergency_contact3,



        contact_count=contact_count



    )



# ====================================================

# INCIDENT REPORT

# ====================================================





@app.route("/incident_report", methods=["GET","POST"])

def incident_report():





    if "user" not in session:



        return redirect("/")







    tourist = Tourist.query.filter_by(



        fullname=session["user"]



    ).first()







    if request.method == "POST":





        incident_type = request.form["incident_type"]



        location = request.form["location"]



        description = request.form["description"]







        severity="Low"



        ai_score=90



        police_required="No"



        medical_required="No"



        response_time="30 Minutes"



        recommendation="Monitor the situation."











        # AI Analysis Rules





        if incident_type=="Medical Emergency":





            severity="High"



            ai_score=25



            medical_required="Yes"



            response_time="5 Minutes"



            recommendation="Ambulance assistance required."









        elif incident_type=="Accident":





            severity="High"



            ai_score=30



            police_required="Yes"



            medical_required="Yes"



            response_time="8 Minutes"



            recommendation="Police and ambulance required."









        elif incident_type=="Theft":





            severity="Medium"



            ai_score=55



            police_required="Yes"



            response_time="15 Minutes"



            recommendation="Report theft to police."









        elif incident_type=="Lost Passport":





            severity="Medium"



            ai_score=65



            police_required="Yes"



            response_time="20 Minutes"



            recommendation="Contact embassy and police."









        elif incident_type=="Harassment":





            severity="High"



            ai_score=35



            police_required="Yes"



            response_time="10 Minutes"



            recommendation="Immediate police assistance."









        elif incident_type=="Natural Disaster":





            severity="Critical"



            ai_score=10



            police_required="Yes"



            medical_required="Yes"



            response_time="Immediate"



            recommendation="Move to evacuation centre."











        report=IncidentReport(





            tourist_name=tourist.fullname,





            incident_type=incident_type,





            location=location,





            description=description,





            report_time=datetime.now().strftime(



                "%d-%m-%Y %H:%M"



            ),





            severity=severity,





            ai_score=ai_score,





            police_required=police_required,





            medical_required=medical_required,





            response_time=response_time,





            recommendation=recommendation



        )







        db.session.add(report)



        db.session.commit()







        return redirect("/incident_report")











    # Dashboard data





    reports=IncidentReport.query.order_by(



        IncidentReport.id.desc()



    ).all()







    total_reports=len(reports)







    low_count=IncidentReport.query.filter_by(



        severity="Low"



    ).count()







    medium_count=IncidentReport.query.filter_by(



        severity="Medium"



    ).count()







    high_count=IncidentReport.query.filter_by(



        severity="High"



    ).count()







    critical_count=IncidentReport.query.filter_by(



        severity="Critical"



    ).count()











    score=tourist.safety_score or 100





    risk=tourist.risk_level or "LOW"





    geo_status=tourist.geo_status or "Unknown"





    location_name=tourist.location_name or "Location Not Available"









    contact_count=0







    if tourist.emergency_contact1:



        contact_count+=1





    if tourist.emergency_contact2:



        contact_count+=1





    if tourist.emergency_contact3:



        contact_count+=1











    analysis={





        "overall_risk":risk,





        "safety_score":score,





        "geo_fence":geo_status,





        "travel_status":tourist.travel_status,





        "night_travel":



            "Yes"



            if datetime.now().hour>=22



            or datetime.now().hour<=5



            else "No",







        "emergency_contacts":contact_count,





        "current_location":location_name,





        "response_time":



            "8 Minutes"



            if "HIGH" in risk



            else



            "15 Minutes"



            if "MEDIUM" in risk



            else



            "25 Minutes",







        "police_required":



            "Yes"



            if "HIGH" in risk



            else "No",







        "medical_required":



            "Yes"



            if score < 40



            else "No",







        "recommendation":



            "Immediate emergency response recommended."



            if "HIGH" in risk



            else



            "Stay alert and avoid isolated places."



            if "MEDIUM" in risk



            else



            "Area appears safe. Continue monitoring."



    }



    tourist_name = tourist.fullname



    return render_template(





        "incident_report.html",





        tourist=tourist,



        tourist_name=tourist_name,



        reports=reports,





        analysis=analysis,





        score=score,





        risk=risk,





        geo_status=geo_status,





        travel_status=tourist.travel_status,





        location_name=location_name,





        contact_count=contact_count,





        total_reports=total_reports,





        low_count=low_count,





        medium_count=medium_count,





        high_count=high_count,





        critical_count=critical_count,





    )



# ====================================================

# ADMIN DASHBOARD

# ====================================================





@app.route("/admin_dashboard")

def admin_dashboard():





    if "admin" not in session:



        return redirect("/admin")







    tourists=Tourist.query.all()







    incidents=IncidentReport.query.order_by(



        IncidentReport.id.desc()



    ).all()







    total_tourists=Tourist.query.count()



    total_contacts=EmergencyContact.query.count()



    total_incidents=IncidentReport.query.count()







    high_risk=Tourist.query.filter(



        Tourist.risk_level.contains("HIGH")



    ).count()







    low_count=IncidentReport.query.filter_by(



        severity="Low"



    ).count()







    medium_count=IncidentReport.query.filter_by(



        severity="Medium"



    ).count()







    high_count=IncidentReport.query.filter_by(



        severity="High"



    ).count()







    critical_count=IncidentReport.query.filter_by(



        severity="Critical"



    ).count()







    return render_template(



        "admin_dashboard.html",



        tourists=tourists,



        incidents=incidents,



        total_tourists=total_tourists,



        total_contacts=total_contacts,



        total_incidents=total_incidents,



        high_risk=high_risk,



        low_count=low_count,



        medium_count=medium_count,



        high_count=high_count,



        critical_count=critical_count



    )











# ====================================================

# ADMIN TOURISTS

# ====================================================





@app.route("/admin_tourists")

def admin_tourists():





    if "admin" not in session:



        return redirect("/admin")







    tourists=Tourist.query.all()







    return render_template(



        "admin_tourists.html",



        tourists=tourists



    )











# ====================================================

# ADMIN INCIDENTS

# ====================================================





@app.route("/admin_incidents")

def admin_incidents():





    if "admin" not in session:



        return redirect("/admin")







    incidents=IncidentReport.query.order_by(



        IncidentReport.id.desc()



    ).all()







    return render_template(



        "admin_incidents.html",



        incidents=incidents



    )











# ====================================================

# ADMIN CONTACTS

# ====================================================





@app.route("/admin_contacts")

def admin_contacts():





    if "admin" not in session:



        return redirect("/admin")







    contacts=EmergencyContact.query.all()







    return render_template(



        "admin_contacts.html",



        contacts=contacts



    )











# ====================================================

# ADMIN GPS MONITORING

# ====================================================





@app.route("/admin_gps")

def admin_gps():





    if "admin" not in session:



        return redirect("/admin")







    tourists=Tourist.query.all()







    return render_template(



        "admin_gps.html",



        tourists=tourists



    )











# ====================================================

# ADMIN AI MONITOR

# ====================================================





@app.route("/admin_ai_monitor")

def admin_ai_monitor():





    if "admin" not in session:



        return redirect("/admin")







    tourists=Tourist.query.all()







    return render_template(



        "admin_ai_monitor.html",



        tourists=tourists



    )











# ====================================================

# ADMIN ANALYTICS

# ====================================================





@app.route("/admin_analytics")

def admin_analytics():





    if "admin" not in session:



        return redirect("/admin")
    
    return render_template(

        "admin_analytics.html",

        total_tourists=Tourist.query.count(),

        total_contacts=EmergencyContact.query.count(),

        total_incidents=IncidentReport.query.count(),

        low_count=IncidentReport.query.filter_by(

            severity="Low"

        ).count(),

        medium_count=IncidentReport.query.filter_by(

            severity="Medium"  ).
            count(),


         high_count=IncidentReport.query.filter_by(

            severity="High"

        ).count(),

        critical_count=IncidentReport.query.filter_by(

            severity="Critical"

        ).count()
    )
# ====================================================

# LOGOUT

# ====================================================

@app.route("/logout")

def logout():
    session.pop("user",None)
    session.pop("admin",None)
    return redirect("/")
# ====================================================

# RUN APPLICATION

# ====================================================

if __name__=="__main__":
    app.run(
        debug=True
    )