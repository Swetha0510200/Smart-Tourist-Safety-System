###############################################################
# ai_engine.py
#
# Tourist Safety Monitoring System
# AI Prediction Engine
###############################################################

from db_helper import get_area_details
from safety_predictor import calculate_real_ai


def predict_risk(
    district,
    emergency_contacts,
    travel_status="Stationary"
):
    """
    Predict tourist safety using district database and AI engine.
    """

    ###########################################################
    # Get District Information
    ###########################################################

    area = get_area_details(district)

    ###########################################################
    # District Not Found
    ###########################################################

    if area is None:

        return {

            "safety_score": 60,

            "risk_level": "MEDIUM",

            "police_required": "No",

            "medical_required": "No",

            "response_time": "20 Minutes",

            "recommendation": "District information is not available."

        }

    ###########################################################
    # Read Database Values
    ###########################################################

    crime_rate = area["crime_rate"]

    lighting_score = area["lighting_score"]

    tourist_density = area["tourist_density"]

    police_distance = area["nearest_police_distance"]

    hospital_distance = area["nearest_hospital_distance"]

    geo_status = area["geo_status"]

    ###########################################################
    # AI Prediction
    ###########################################################

    result = calculate_real_ai(

        crime_rate,

        lighting_score,

        tourist_density,

        police_distance,

        hospital_distance,

        emergency_contacts,

        geo_status,

        travel_status

    )

    ###########################################################
    # Return AI Result
    ###########################################################

    return result