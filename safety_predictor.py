###############################################################
# safety_predictor.py
#
# Smart Tourist Safety Monitoring System
# AI Safety Prediction Engine
###############################################################

from datetime import datetime


def calculate_real_ai(
    crime_rate,
    lighting_score,
    tourist_density,
    police_distance,
    hospital_distance,
    emergency_contacts,
    geo_status,
    travel_status
):
    """
    Returns:

    safety_score
    risk_level
    police_required
    medical_required
    response_time
    recommendation
    """

    ###############################################################
    # Initial Score
    ###############################################################

    score = 100

    ###############################################################
    # Crime Rate
    ###############################################################

    if crime_rate >= 80:
        score -= 35

    elif crime_rate >= 60:
        score -= 25

    elif crime_rate >= 40:
        score -= 15

    elif crime_rate >= 20:
        score -= 5

    ###############################################################
    # Lighting
    ###############################################################

    if lighting_score < 20:
        score -= 25

    elif lighting_score < 40:
        score -= 15

    elif lighting_score < 60:
        score -= 8

    ###############################################################
    # Tourist Density
    ###############################################################

    if tourist_density < 20:
        score -= 20

    elif tourist_density < 40:
        score -= 10

    ###############################################################
    # Police Distance
    ###############################################################

    if police_distance > 15:
        score -= 20

    elif police_distance > 10:
        score -= 15

    elif police_distance > 5:
        score -= 8

    ###############################################################
    # Hospital Distance
    ###############################################################

    if hospital_distance > 15:
        score -= 20

    elif hospital_distance > 10:
        score -= 12

    elif hospital_distance > 5:
        score -= 5

    ###############################################################
    # Emergency Contacts
    ###############################################################

    if emergency_contacts == 0:
        score -= 15

    elif emergency_contacts == 1:
        score -= 8

    elif emergency_contacts >= 3:
        score += 5

    ###############################################################
    # Geo Fence
    ###############################################################

    if "Unsafe" in geo_status:
        score -= 20

    elif "Warning" in geo_status:
        score -= 10

    ###############################################################
    # Night Travel
    ###############################################################

    hour = datetime.now().hour

    if hour >= 22 or hour <= 5:
        score -= 15

    ###############################################################
    # Travel Status
    ###############################################################

    if travel_status == "Travelling":
        score -= 5
    elif travel_status == "Stationary":
        score += 2

    ###############################################################
    # Score Limits
    ###############################################################

    if score > 100:
        score = 100

    if score < 0:
        score = 0

    ###############################################################
    # Risk Level
    ###############################################################

    if score >= 80:

        risk = "LOW"

        police_required = "No"
        medical_required = "No"

        response_time = "25 Minutes"

        recommendation = (
            "Area appears safe. Continue your journey. "
            "Keep GPS enabled and remain alert."
        )

    elif score >= 55:

        risk = "MEDIUM"

        police_required = "Optional"
        medical_required = "No"

        response_time = "15 Minutes"

        recommendation = (
            "Avoid isolated places. Stay in public areas. "
            "Share your location with emergency contacts."
        )

    elif score >= 35:

        risk = "HIGH"

        police_required = "Yes"
        medical_required = "Possible"

        response_time = "8 Minutes"

        recommendation = (
            "Move towards the nearest safe zone immediately. "
            "Avoid travelling alone."
        )

    else:

        risk = "CRITICAL"

        police_required = "Yes"
        medical_required = "Yes"

        response_time = "Immediate"

        recommendation = (
            "Emergency detected. Use SOS immediately. "
            "Police and medical assistance required."
        )

    ###############################################################
    # Final Result
    ###############################################################

    return {

        "safety_score": score,

        "risk_level": risk,

        "police_required": police_required,

        "medical_required": medical_required,

        "response_time": response_time,

        "recommendation": recommendation

    }