from datetime import datetime, date, timedelta
from flask import Blueprint, request, jsonify, session
from models import db, Driver, Vehicle, Customer, Memo, MemoExpense, FuelBill
from financial_calculator import calculate_financials
from fuel_theft_detector import analyze_fuel_consumption

api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route('/calculate', methods=['POST'])
def calculate_api():
    """Real-time financial calculator API used by client-side interactive forms"""
    data = request.get_json() or {}
    freight = float(data.get('freight_amount', 0.0) or 0.0)
    advance = float(data.get('advance_amount', 0.0) or 0.0)
    diesel = float(data.get('diesel_expense', 0.0) or 0.0)
    toll = float(data.get('toll_expense', 0.0) or 0.0)
    food = float(data.get('food_expense', 0.0) or 0.0)
    loading = float(data.get('loading_charges', 0.0) or 0.0)
    unloading = float(data.get('unloading_charges', 0.0) or 0.0)
    other = float(data.get('other_expenses', 0.0) or 0.0)

    result = calculate_financials(freight, advance, diesel, toll, food, loading, unloading, other)
    return jsonify(result)

@api_bp.route('/analytics/charts')
def analytics_charts():
    """
    Returns structured data for the 8 dashboard charts:
    1. Monthly Revenue
    2. Monthly Expenses
    3. Monthly Profit
    4. Vehicle-wise Revenue
    5. Vehicle-wise Expenses
    6. Driver-wise Performance
    7. Fuel Consumption Analysis
    8. Profit vs Expense Comparison
    """
    # 1. Month-by-month aggregates for current year
    month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    monthly_rev = [0.0] * 12
    monthly_exp = [0.0] * 12
    monthly_prof = [0.0] * 12

    all_memos = Memo.query.all()
    for m in all_memos:
        if m.memo_date:
            m_idx = m.memo_date.month - 1
            monthly_rev[m_idx] += m.freight_amount
            monthly_exp[m_idx] += m.total_expense
            monthly_prof[m_idx] += m.profit

    # 2. Vehicle-wise Revenue & Expense
    vehicles = Vehicle.query.all()
    veh_labels = []
    veh_revs = []
    veh_exps = []
    for v in vehicles:
        v_memos = Memo.query.filter_by(vehicle_id=v.id).all()
        veh_labels.append(v.vehicle_number)
        veh_revs.append(sum(m.freight_amount for m in v_memos))
        veh_exps.append(sum(m.total_expense for m in v_memos))

    # 3. Driver-wise Performance
    drivers = Driver.query.all()
    drv_labels = []
    drv_trips = []
    drv_revenue = []
    for d in drivers:
        d_memos = Memo.query.filter_by(driver_id=d.id).all()
        drv_labels.append(d.full_name)
        drv_trips.append(len(d_memos))
        drv_revenue.append(sum(m.freight_amount for m in d_memos))

    # 4. Fuel Consumption (Expected vs Actual Liters)
    fuel_memo_labels = []
    fuel_expected = []
    fuel_actual = []
    for m in all_memos[-6:]: # Last 6 memos
        analysis = analyze_fuel_consumption(m, m.vehicle)
        fuel_memo_labels.append(m.memo_number)
        fuel_expected.append(analysis['expected_liters'])
        fuel_actual.append(analysis['actual_liters'])

    # 5. Profit vs Expense Comparison Totals
    total_rev = sum(monthly_rev)
    total_exp = sum(monthly_exp)
    total_prof = sum(m for m in monthly_prof if m > 0)
    total_loss = sum(abs(m) for m in monthly_prof if m < 0)

    return jsonify({
        "months": month_names,
        "monthly_revenue": monthly_rev,
        "monthly_expenses": monthly_exp,
        "monthly_profit": monthly_prof,
        "vehicles": {
            "labels": veh_labels,
            "revenue": veh_revs,
            "expenses": veh_exps
        },
        "drivers": {
            "labels": drv_labels,
            "trips": drv_trips,
            "revenue": drv_revenue
        },
        "fuel_analysis": {
            "labels": fuel_memo_labels,
            "expected": fuel_expected,
            "actual": fuel_actual
        },
        "totals": {
            "revenue": total_rev,
            "expenses": total_exp,
            "profit": total_prof,
            "loss": total_loss
        }
    })

@api_bp.route('/search')
def global_search():
    q = request.args.get('q', '').strip()
    if not q or len(q) < 2:
        return jsonify({"results": []})

    results = []

    # Drivers
    drivers = Driver.query.filter(
        (Driver.full_name.ilike(f"%{q}%")) |
        (Driver.driver_code.ilike(f"%{q}%")) |
        (Driver.phone.ilike(f"%{q}%"))
    ).limit(5).all()
    for d in drivers:
        results.append({
            "category": "Driver",
            "title": f"{d.full_name} ({d.driver_code})",
            "subtitle": f"Phone: {d.phone} | License: {d.license_number}",
            "url": f"/admin/drivers/{d.id}/details"
        })

    # Vehicles
    vehicles = Vehicle.query.filter(
        (Vehicle.vehicle_number.ilike(f"%{q}%")) |
        (Vehicle.model.ilike(f"%{q}%")) |
        (Vehicle.rc_number.ilike(f"%{q}%"))
    ).limit(5).all()
    for v in vehicles:
        results.append({
            "category": "Vehicle",
            "title": v.vehicle_number,
            "subtitle": f"{v.model or v.vehicle_type} | Capacity: {v.capacity}",
            "url": f"/admin/vehicles/{v.id}/details"
        })

    # Memos
    memos = Memo.query.filter(
        (Memo.memo_number.ilike(f"%{q}%")) |
        (Memo.source.ilike(f"%{q}%")) |
        (Memo.destination.ilike(f"%{q}%"))
    ).limit(5).all()
    for m in memos:
        results.append({
            "category": "Memo",
            "title": f"{m.memo_number}: {m.source} -> {m.destination}",
            "subtitle": f"Date: {m.memo_date} | Profit: Rs. {m.profit:,.2f} ({m.status})",
            "url": f"/admin/memos/{m.id}"
        })

    # Customers
    customers = Customer.query.filter(
        (Customer.company_name.ilike(f"%{q}%")) |
        (Customer.contact_person.ilike(f"%{q}%")) |
        (Customer.mobile_number.ilike(f"%{q}%"))
    ).limit(5).all()
    for c in customers:
        results.append({
            "category": "Customer",
            "title": c.company_name,
            "subtitle": f"Contact: {c.contact_person} ({c.mobile_number})",
            "url": "/driver/customers"
        })

    return jsonify({"results": results})

@api_bp.route('/memos/extract', methods=['POST'])
def extract_memo_api():
    """
    Public / Integration API endpoint for Automatic Handwritten Memo OCR & Extraction.
    Accepts image file via multipart form-data (field 'memo_file' or 'sample_choice').
    Returns strict JSON adhering to Section 18 specification with validation checks.
    """
    import os
    import shutil
    from flask import url_for, current_app
    from config import Config
    from image_enhancer import preprocess_memo_image
    from services.handwriting_ocr_service import HandwritingOCRService
    from services.ai_extraction_service import AIExtractionService
    from services.validation_service import ValidationService

    file = request.files.get('memo_file')
    sample_choice = request.form.get('sample_choice')

    timestamp = int(datetime.now().timestamp())
    if sample_choice:
        src_path = os.path.join(Config.BASE_DIR, 'static', 'sample_memos', sample_choice)
        if not os.path.exists(src_path):
            return jsonify({"error": f"Sample memo '{sample_choice}' not found"}), 404
        safe_name = f"api_memo_{timestamp}_{sample_choice}"
        save_path = os.path.join(Config.MEMO_UPLOAD_FOLDER, safe_name)
        shutil.copyfile(src_path, save_path)
        rel_path = f"uploads/memos/{safe_name}"
    elif file and file.filename != '':
        ext = file.filename.rsplit('.', 1)[-1].lower()
        if ext not in Config.ALLOWED_EXTENSIONS:
            return jsonify({"error": f"Invalid extension '{ext}'. Allowed: JPG, PNG, WEBP, PDF"}), 400
        safe_name = f"api_memo_{timestamp}.{ext}"
        save_path = os.path.join(Config.MEMO_UPLOAD_FOLDER, safe_name)
        file.save(save_path)
        rel_path = f"uploads/memos/{safe_name}"
    else:
        return jsonify({"error": "No file or sample_choice provided in request"}), 400

    # 1. Preprocess
    prep_res = preprocess_memo_image(save_path)
    enhanced_path = prep_res[0]
    binarized_path = prep_res[1]
    enhanced_rel = f"uploads/memos/{os.path.basename(enhanced_path)}" if os.path.exists(enhanced_path) else rel_path
    binarized_rel = f"uploads/memos/{os.path.basename(binarized_path)}" if os.path.exists(binarized_path) else rel_path

    # 2. OCR
    ocr_res = HandwritingOCRService.extract_text(enhanced_path or save_path, languages=['ta', 'en'], original_image_path=save_path)

    # 3. AI Extraction
    extracted = AIExtractionService.extract_memo_data(ocr_res)

    # 4. Validation
    validation = ValidationService.validate_memo(extracted)

    # Return strict Section 18 JSON structure with metadata
    response_data = {
        "status": "success",
        "data": extracted,
        "validation": validation,
        "metadata": {
            "engine": getattr(ocr_res, 'engine', 'EasyOCR (Tamil+English)'),
            "raw_text_length": len(ocr_res.full_text),
            "image_url": f"/static/{rel_path}",
            "enhanced_image_url": f"/static/{enhanced_rel}",
            "binarized_image_url": f"/static/{binarized_rel}"
        }
    }
    return jsonify(response_data)

