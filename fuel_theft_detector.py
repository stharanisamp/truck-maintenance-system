import math
from models import Notification, db

# Estimated highway distance between common industrial hubs (in km)
ROUTE_DISTANCES = {
    ("chennai", "madurai"): 460,
    ("madurai", "chennai"): 460,
    ("salem", "coimbatore"): 160,
    ("coimbatore", "salem"): 160,
    ("ariyalur", "chennai"): 310,
    ("chennai", "ariyalur"): 310,
    ("hosur", "tuticorin"): 520,
    ("tuticorin", "hosur"): 520,
    ("chennai", "bangalore"): 350,
    ("bangalore", "chennai"): 350,
    ("trichy", "chennai"): 330,
    ("chennai", "trichy"): 330,
    ("salem", "chennai"): 340,
    ("chennai", "salem"): 340
}

def estimate_trip_distance(source, destination):
    """Estimates distance in KM between source and destination, with fallback"""
    s = (source or "").strip().lower()
    d = (destination or "").strip().lower()
    if (s, d) in ROUTE_DISTANCES:
        return ROUTE_DISTANCES[(s, d)]
    # Reasonable default commercial trip distance
    return 350

def analyze_fuel_consumption(memo, vehicle=None, fuel_bills=None):
    """
    Analyzes fuel consumption for a trip memo:
    - Expected mileage: 3.5 km/liter (typical heavy lorry average in India)
    - Average Diesel price: 95.0 Rs/Liter
    - Expected fuel (Liters) = Distance / 3.5
    - Actual fuel (Liters):
        If fuel bills linked to memo exist, sum their liters.
        Otherwise derived from memo.expense.diesel_expense / 95.0
    - Fuel difference = Actual - Expected
    - Percentage discrepancy = (Fuel difference / Expected) * 100
    - Risk Level:
        <= 5%: Normal
        5% to 15%: Warning
        > 15%: High Risk
    """
    distance = estimate_trip_distance(memo.source, memo.destination)
    expected_mileage = 3.5  # km per liter
    avg_diesel_rate = 95.0  # Rs per liter

    expected_liters = round(distance / expected_mileage, 2)
    expected_cost = round(expected_liters * avg_diesel_rate, 2)

    actual_liters = 0.0
    actual_cost = 0.0

    # Check fuel bills first
    if fuel_bills and len(fuel_bills) > 0:
        actual_liters = sum(fb.fuel_quantity for fb in fuel_bills)
        actual_cost = sum(fb.total_amount for fb in fuel_bills)
    elif memo.expense and memo.expense.diesel_expense > 0:
        actual_cost = memo.expense.diesel_expense
        actual_liters = round(actual_cost / avg_diesel_rate, 2)
    else:
        actual_liters = expected_liters
        actual_cost = expected_cost

    diff_liters = round(actual_liters - expected_liters, 2)
    diff_cost = round(actual_cost - expected_cost, 2)
    
    if expected_liters > 0:
        pct_diff = round((diff_liters / expected_liters) * 100, 1)
    else:
        pct_diff = 0.0

    if pct_diff > 15.0:
        risk_level = "High Risk"
        is_suspicious = True
    elif pct_diff > 5.0:
        risk_level = "Warning"
        is_suspicious = True
    else:
        risk_level = "Normal"
        is_suspicious = False

    return {
        "memo_id": memo.id,
        "memo_number": memo.memo_number,
        "source": memo.source,
        "destination": memo.destination,
        "distance_km": distance,
        "expected_liters": expected_liters,
        "actual_liters": round(actual_liters, 2),
        "diff_liters": diff_liters,
        "expected_cost": expected_cost,
        "actual_cost": actual_cost,
        "diff_cost": diff_cost,
        "pct_diff": pct_diff,
        "risk_level": risk_level,
        "is_suspicious": is_suspicious
    }

def check_and_create_fuel_alert(analysis, driver_name=None, vehicle_no=None):
    """Creates a system notification if fuel consumption is suspicious"""
    if analysis["is_suspicious"]:
        title = f"Fuel Anomaly Detected: {analysis['risk_level']}"
        msg = (
            f"Trip {analysis['memo_number']} ({analysis['source']} -> {analysis['destination']}) "
            f"by {driver_name or 'Driver'} on vehicle {vehicle_no or 'Lorry'}: "
            f"Actual Fuel {analysis['actual_liters']} L vs Expected {analysis['expected_liters']} L "
            f"(+{analysis['pct_diff']}%). Potential fuel pilferage!"
        )
        notif = Notification(
            title=title,
            message=msg,
            alert_type="FUEL_THEFT",
            severity=analysis["risk_level"],
            link="/admin/fuel-monitoring"
        )
        db.session.add(notif)
        db.session.commit()
        return notif
    return None
