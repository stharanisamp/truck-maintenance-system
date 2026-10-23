import re
from datetime import datetime, date
from typing import Dict, Any, List

class ValidationService:
    """
    Independent Validation & Consistency Engine for Lorry Memo Extractions.
    Applies mathematical validation, vehicle format verification, calendar checks,
    suspicious value detection, and field confidence level categorization.
    """

    INDIAN_STATES = {
        'AN', 'AP', 'AR', 'AS', 'BR', 'CH', 'CG', 'DD', 'DL', 'DN', 'GA', 'GJ',
        'HR', 'HP', 'JH', 'JK', 'KA', 'KL', 'LA', 'LD', 'MP', 'MH', 'MN', 'ML',
        'MZ', 'NL', 'OD', 'PB', 'PY', 'RJ', 'SK', 'TN', 'TS', 'TR', 'UP', 'UK', 'WB'
    }

    CONFIDENCE_HIGH = 0.85
    CONFIDENCE_MEDIUM = 0.60

    @classmethod
    def validate_memo(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Runs comprehensive multi-dimensional validation on extracted memo data:
        1. Mathematical reconciliation of expenses
        2. Indian vehicle registration validation
        3. Calendar date validation
        4. Suspicious numeric values (e.g. extra zeros)
        5. Required fields completeness check
        6. Confidence level binning (high, medium, low)
        """
        warnings = []
        field_status = {}
        math_check = {}

        # 1. Mathematical Validation
        fuel = data.get("fuel_expense") or 0.0
        toll = data.get("toll_expense") or 0.0
        loading = data.get("loading_charge") or 0.0
        unloading = data.get("unloading_charge") or 0.0
        food = data.get("food_expense") or 0.0
        parking = data.get("parking_expense") or 0.0
        repair = data.get("repair_expense") or 0.0
        other = data.get("other_expense") or 0.0

        calculated_total = round(fuel + toll + loading + unloading + food + parking + repair + other, 2)
        handwritten_total = data.get("total_expense")

        math_check = {
            "calculated_total": calculated_total,
            "handwritten_total": handwritten_total,
            "is_matched": True,
            "difference": 0.0
        }

        if handwritten_total is not None and calculated_total > 0:
            diff = round(abs(calculated_total - handwritten_total), 2)
            math_check["difference"] = diff
            if diff > 10.0:
                math_check["is_matched"] = False
                warnings.append({
                    "field": "total_expense",
                    "type": "MATH_MISMATCH",
                    "message": (
                        f"Expense mismatch: Sum of itemized expenses is ₹{calculated_total:,.2f}, "
                        f"but handwritten total shows ₹{handwritten_total:,.2f} (Difference: ₹{diff:,.2f}). "
                        "Please verify."
                    ),
                    "tamil_message": f"செலவு கூடுதல் ₹{calculated_total:,.2f} ஆனால் சீட்டில் ₹{handwritten_total:,.2f} உள்ளது."
                })

        # 2. Vehicle Registration Validation
        veh = data.get("vehicle_number")
        if veh:
            m = re.match(r'^([A-Z]{2})\s*(\d{1,2})\s*([A-Z]{1,3})\s*(\d{4})$', veh.replace("-", " ").strip().upper())
            if m:
                state_code = m.group(1)
                if state_code not in cls.INDIAN_STATES:
                    warnings.append({
                        "field": "vehicle_number",
                        "type": "INVALID_STATE_CODE",
                        "message": f"State code '{state_code}' in vehicle {veh} is not a standard Indian state code.",
                        "tamil_message": f"வண்டி எண் மாநில குறியீடு '{state_code}' சரியா என சரிபார்க்கவும்."
                    })
            else:
                warnings.append({
                    "field": "vehicle_number",
                    "type": "IRREGULAR_PLATE_FORMAT",
                    "message": f"Vehicle number '{veh}' does not follow standard Indian registration pattern (e.g. TN 52 AB 1234).",
                    "tamil_message": "வண்டி எண் வடிவம் சரியாக இல்லை. சரிபார்க்கவும்."
                })
        else:
            warnings.append({
                "field": "vehicle_number",
                "type": "REQUIRED_MISSING",
                "message": "Vehicle number could not be detected from memo handwriting. Please select or enter.",
                "tamil_message": "வண்டி எண் கண்டறியப்படவில்லை. உள்ளிடவும்."
            })

        # 3. Calendar Date Validation
        memo_dt_str = data.get("date")
        if memo_dt_str:
            try:
                memo_dt = datetime.strptime(memo_dt_str, '%Y-%m-%d').date()
                today = date.today()
                if memo_dt > today:
                    warnings.append({
                        "field": "date",
                        "type": "FUTURE_DATE",
                        "message": f"Extracted memo date {memo_dt_str} is in the future. Please confirm.",
                        "tamil_message": f"தேதி {memo_dt_str} எதிர்கால தேதியாக உள்ளது. சரிபார்க்கவும்."
                    })
                elif (today - memo_dt).days > 365:
                    warnings.append({
                        "field": "date",
                        "type": "OLD_DATE",
                        "message": f"Memo date {memo_dt_str} is more than 1 year ago. Please verify.",
                        "tamil_message": f"தேதி {memo_dt_str} ஒரு வருடத்திற்கு முந்தையதாக உள்ளது."
                    })
            except ValueError:
                warnings.append({
                    "field": "date",
                    "type": "INVALID_DATE",
                    "message": f"Invalid calendar date extracted: '{memo_dt_str}'.",
                    "tamil_message": "தவறான தேதி வடிவம்."
                })
        else:
            warnings.append({
                "field": "date",
                "type": "REQUIRED_MISSING",
                "message": "Memo date is missing. Defaulting to today's date for review.",
                "tamil_message": "தேதி இல்லை. இன்றைய தேதி தேர்வு செய்யப்பட்டுள்ளது."
            })

        # 4. Suspicious Numeric Sanity Checks (e.g. Extra Zeros)
        # Typical truck trip single expense range check:
        # Single diesel refill is rarely > ₹75,000 for normal lorry trip
        if fuel > 75000.0:
            warnings.append({
                "field": "fuel_expense",
                "type": "SUSPICIOUS_HIGH_VALUE",
                "message": f"Fuel expense ₹{fuel:,.2f} is unusually high. Check for an accidental extra zero.",
                "tamil_message": f"டீசல் தொகை ₹{fuel:,.2f} வழக்கத்திற்கு மாறாக அதிகமாக உள்ளது. கூடுதல் பூஜ்ஜியம் உள்ளதா என பார்க்கவும்."
            })

        if toll > 15000.0:
            warnings.append({
                "field": "toll_expense",
                "type": "SUSPICIOUS_HIGH_VALUE",
                "message": f"Toll expense ₹{toll:,.2f} is unusually high. Please verify.",
                "tamil_message": f"சுங்க கட்டணம் ₹{toll:,.2f} வழக்கத்திற்கு மாறாக அதிகமாக உள்ளது."
            })

        if food > 8000.0:
            warnings.append({
                "field": "food_expense",
                "type": "SUSPICIOUS_HIGH_VALUE",
                "message": f"Driver food/bata allowance ₹{food:,.2f} is unusually high. Please verify.",
                "tamil_message": f"சாப்பாடு/படி ₹{food:,.2f} வழக்கத்திற்கு மாறாக அதிகமாக உள்ளது."
            })

        # 5. Required Fields Completeness Check
        required_fields = [
            ("vehicle_number", "Vehicle Number"),
            ("date", "Memo Date"),
            ("driver_name", "Driver Name"),
            ("from_place", "Trip Origin (From)"),
            ("to_place", "Trip Destination (To)"),
            ("trip_amount", "Freight Amount")
        ]

        missing_required = []
        for f_key, f_label in required_fields:
            if not data.get(f_key):
                missing_required.append(f_label)

        if missing_required:
            warnings.append({
                "field": "general",
                "type": "INCOMPLETE_FIELDS",
                "message": f"Unfilled core fields: {', '.join(missing_required)}. Please fill before final save.",
                "tamil_message": f"முக்கிய விவரங்கள் விடுபட்டுள்ளன: {', '.join(missing_required)}."
            })

        # 6. Confidence Categorization per Field
        conf_map = data.get("confidence", {})
        all_keys = [
            "vehicle_number", "date", "memo_number", "driver_name", "driver_phone",
            "from_place", "to_place", "fuel_expense", "toll_expense", "loading_charge",
            "unloading_charge", "food_expense", "trip_amount", "driver_advance", "total_expense"
        ]

        for k in all_keys:
            val = data.get(k)
            score = conf_map.get(k, 0.5 if val else 0.0)
            if not val:
                field_status[k] = {"level": "empty", "score": 0.0, "label": "Not Present"}
            elif score >= cls.CONFIDENCE_HIGH:
                field_status[k] = {"level": "high", "score": score, "label": "High Confidence"}
            elif score >= cls.CONFIDENCE_MEDIUM:
                field_status[k] = {"level": "medium", "score": score, "label": "Needs Review"}
            else:
                field_status[k] = {"level": "low", "score": score, "label": "Uncertain (Verify)"}

        # Overall validation status
        if any(w["type"] in ["MATH_MISMATCH", "SUSPICIOUS_HIGH_VALUE", "INCOMPLETE_FIELDS"] for w in warnings):
            overall_status = "WARNINGS"
        elif any(f["level"] == "low" for f in field_status.values()):
            overall_status = "NEEDS_REVIEW"
        else:
            overall_status = "VALID"

        return {
            "is_valid": len(warnings) == 0,
            "status": overall_status,
            "warnings": warnings,
            "math_check": math_check,
            "field_status": field_status,
            "has_mismatch": not math_check.get("is_matched", True)
        }
