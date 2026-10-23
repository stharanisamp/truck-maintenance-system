from datetime import datetime, date, timedelta
from functools import wraps
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, send_file, jsonify
from models import db, Admin, Driver, Vehicle, Customer, Memo, MemoExpense, FuelBill, Notification, ActivityLog
from fuel_theft_detector import analyze_fuel_consumption
try:
    from report_generator import generate_pdf_report, generate_docx_report
except Exception:
    generate_pdf_report = None
    generate_docx_report = None

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('role') != 'admin' or not session.get('user_id'):
            flash("Admin login required to access this area.", "warning")
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/dashboard')
@admin_required
def dashboard():
    # 1. 10 KPI Cards
    total_drivers = Driver.query.count()
    total_vehicles = Vehicle.query.count()
    total_customers = Customer.query.count()
    total_memos = Memo.query.count()
    total_fuel_bills = FuelBill.query.count()

    all_memos = Memo.query.all()
    total_revenue = sum(m.freight_amount for m in all_memos)
    total_expenses = sum(m.total_expense for m in all_memos)
    
    total_profit = sum(m.profit for m in all_memos if m.profit > 0)
    total_loss = sum(abs(m.profit) for m in all_memos if m.profit < 0)

    suspicious_alerts_count = Notification.query.filter_by(alert_type="FUEL_THEFT").count()
    unread_notifications_count = Notification.query.filter_by(is_read=False).count()

    # 2. Recent Activities
    recent_memos = Memo.query.order_by(Memo.id.desc()).limit(5).all()
    recent_drivers = Driver.query.order_by(Driver.id.desc()).limit(5).all()
    recent_vehicles = Vehicle.query.order_by(Vehicle.id.desc()).limit(5).all()
    recent_fuel_bills = FuelBill.query.order_by(FuelBill.id.desc()).limit(5).all()
    recent_notifications = Notification.query.order_by(Notification.id.desc()).limit(5).all()
    recent_logs = ActivityLog.query.order_by(ActivityLog.id.desc()).limit(8).all()

    # 3. Dynamic Alerts Inspection (Insurance expiry, license expiry, fuel theft)
    today = date.today()
    expiring_insurance = Vehicle.query.filter(Vehicle.insurance_expiry_date <= today + timedelta(days=30)).all()
    expiring_licenses = Driver.query.filter(Driver.license_expiry_date <= today + timedelta(days=30)).all()

    return render_template(
        'admin/dashboard.html',
        total_drivers=total_drivers,
        total_vehicles=total_vehicles,
        total_customers=total_customers,
        total_revenue=total_revenue,
        total_expenses=total_expenses,
        total_profit=total_profit,
        total_loss=total_loss,
        total_memos=total_memos,
        total_fuel_bills=total_fuel_bills,
        suspicious_alerts_count=suspicious_alerts_count,
        unread_notifications_count=unread_notifications_count,
        recent_memos=recent_memos,
        recent_drivers=recent_drivers,
        recent_vehicles=recent_vehicles,
        recent_fuel_bills=recent_fuel_bills,
        recent_notifications=recent_notifications,
        recent_logs=recent_logs,
        expiring_insurance=expiring_insurance,
        expiring_licenses=expiring_licenses
    )

# ----------------- DRIVER MAINTENANCE -----------------
@admin_bp.route('/drivers')
@admin_required
def drivers():
    query = request.args.get('q', '').strip()
    status_filter = request.args.get('status', '')
    
    driver_query = Driver.query
    if query:
        driver_query = driver_query.filter(
            (Driver.full_name.ilike(f"%{query}%")) |
            (Driver.driver_code.ilike(f"%{query}%")) |
            (Driver.license_number.ilike(f"%{query}%")) |
            (Driver.phone.ilike(f"%{query}%"))
        )
    if status_filter:
        driver_query = driver_query.filter_by(status=status_filter)
        
    driver_list = driver_query.order_by(Driver.id.desc()).all()
    return render_template('admin/drivers.html', drivers=driver_list, query=query, status_filter=status_filter)

@admin_bp.route('/drivers/add', methods=['GET', 'POST'])
@admin_required
def add_driver():
    if request.method == 'POST':
        driver_code = request.form.get('driver_code', '').strip().upper()
        full_name = request.form.get('full_name', '').strip()
        email = request.form.get('email', '').strip().lower()
        phone = request.form.get('phone', '').strip()
        address = request.form.get('address', '').strip()
        license_number = request.form.get('license_number', '').strip().upper()
        lic_exp_str = request.form.get('license_expiry_date', '').strip()
        dob_str = request.form.get('date_of_birth', '').strip()
        password = request.form.get('password', 'driver123').strip()
        status = request.form.get('status', 'Active')

        if not driver_code:
            driver_code = f"DRV-{Driver.query.count() + 1:03d}"

        if Driver.query.filter_by(email=email).first():
            flash("Email already registered.", "danger")
            return redirect(url_for('admin.add_driver'))

        d = Driver(
            driver_code=driver_code,
            full_name=full_name,
            email=email,
            phone=phone,
            address=address,
            license_number=license_number,
            status=status
        )
        if lic_exp_str:
            try:
                d.license_expiry_date = datetime.strptime(lic_exp_str, '%Y-%m-%d').date()
            except ValueError:
                pass
        if dob_str:
            try:
                d.date_of_birth = datetime.strptime(dob_str, '%Y-%m-%d').date()
            except ValueError:
                pass

        d.set_password(password)
        db.session.add(d)
        db.session.commit()
        flash(f"Driver {full_name} ({driver_code}) created successfully.", "success")
        return redirect(url_for('admin.drivers'))

    next_code = f"DRV-{Driver.query.count() + 1:03d}"
    return render_template('admin/driver_form.html', action="Add", driver=None, next_code=next_code)

@admin_bp.route('/drivers/<int:driver_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_driver(driver_id):
    driver = Driver.query.get_or_404(driver_id)
    if request.method == 'POST':
        driver.full_name = request.form.get('full_name', driver.full_name).strip()
        driver.email = request.form.get('email', driver.email).strip().lower()
        driver.phone = request.form.get('phone', driver.phone).strip()
        driver.address = request.form.get('address', driver.address).strip()
        driver.license_number = request.form.get('license_number', driver.license_number).strip().upper()
        driver.status = request.form.get('status', driver.status)
        
        lic_exp_str = request.form.get('license_expiry_date', '').strip()
        if lic_exp_str:
            try:
                driver.license_expiry_date = datetime.strptime(lic_exp_str, '%Y-%m-%d').date()
            except ValueError:
                pass

        new_pass = request.form.get('password', '').strip()
        if new_pass:
            driver.set_password(new_pass)

        db.session.commit()
        flash(f"Driver {driver.full_name} updated successfully.", "success")
        return redirect(url_for('admin.drivers'))

    return render_template('admin/driver_form.html', action="Edit", driver=driver)

@admin_bp.route('/drivers/<int:driver_id>/details')
@admin_required
def driver_details(driver_id):
    driver = Driver.query.get_or_404(driver_id)
    driver_memos = Memo.query.filter_by(driver_id=driver_id).order_by(Memo.id.desc()).all()
    driver_customers = Customer.query.filter_by(driver_id=driver_id).all()
    driver_fuel = FuelBill.query.filter_by(driver_id=driver_id).all()

    total_revenue = sum(m.freight_amount for m in driver_memos)
    total_expense = sum(m.total_expense for m in driver_memos)
    total_profit = sum(m.profit for m in driver_memos)

    return render_template(
        'admin/driver_details.html',
        driver=driver,
        memos=driver_memos,
        customers=driver_customers,
        fuel_bills=driver_fuel,
        total_revenue=total_revenue,
        total_expense=total_expense,
        total_profit=total_profit
    )

@admin_bp.route('/drivers/<int:driver_id>/delete', methods=['POST'])
@admin_required
def delete_driver(driver_id):
    driver = Driver.query.get_or_404(driver_id)
    name = driver.full_name
    db.session.delete(driver)
    db.session.commit()
    flash(f"Driver {name} deleted successfully.", "info")
    return redirect(url_for('admin.drivers'))

# ----------------- VEHICLE MANAGEMENT MODULE -----------------
@admin_bp.route('/vehicles')
@admin_required
def vehicles():
    query = request.args.get('q', '').strip()
    status_filter = request.args.get('status', '').strip()
    direct_search = request.args.get('direct', '').strip()

    # Normalize query for direct vehicle number matching (e.g. "tn28ab1234" or "TN 28 AB 1234")
    norm_query = query.replace(" ", "").upper()

    v_query = Vehicle.query
    if query:
        # Check if direct search or exact vehicle number lookup was requested
        if direct_search or len(norm_query) >= 4:
            exact_match = Vehicle.query.filter(
                db.func.replace(Vehicle.vehicle_number, ' ', '').ilike(norm_query)
            ).first()
            if exact_match and (direct_search or exact_match.vehicle_number.replace(' ', '').upper() == norm_query):
                flash(f"Vehicle Intelligence found for {exact_match.vehicle_number}", "info")
                return redirect(url_for('admin.vehicle_details', vehicle_id=exact_match.id))

        v_query = v_query.filter(
            (Vehicle.vehicle_number.ilike(f"%{query}%")) |
            (Vehicle.model.ilike(f"%{query}%")) |
            (Vehicle.brand.ilike(f"%{query}%")) |
            (Vehicle.rc_number.ilike(f"%{query}%")) |
            (Vehicle.chassis_number.ilike(f"%{query}%")) |
            (Vehicle.engine_number.ilike(f"%{query}%"))
        )

    if status_filter:
        if status_filter == 'Maintenance':
            v_query = v_query.filter(Vehicle.status.in_(['Maintenance', 'In Maintenance']))
        else:
            v_query = v_query.filter(Vehicle.status == status_filter)

    vehicle_list = v_query.order_by(Vehicle.id.desc()).all()

    # Status summary counts
    total_vehicles = Vehicle.query.count()
    active_count = Vehicle.query.filter_by(status='Active').count()
    maintenance_count = Vehicle.query.filter(Vehicle.status.in_(['In Maintenance', 'Maintenance'])).count()
    trip_count = Vehicle.query.filter_by(status='In Trip').count()
    inactive_count = Vehicle.query.filter_by(status='Inactive').count()

    today = date.today()

    return render_template(
        'admin/vehicles.html',
        vehicles=vehicle_list,
        query=query,
        status_filter=status_filter,
        total_vehicles=total_vehicles,
        active_count=active_count,
        maintenance_count=maintenance_count,
        trip_count=trip_count,
        inactive_count=inactive_count,
        today=today
    )

@admin_bp.route('/vehicles/add', methods=['GET', 'POST'])
@admin_required
def add_vehicle():
    drivers = Driver.query.filter_by(status='Active').order_by(Driver.full_name).all()
    if request.method == 'POST':
        veh_num = request.form.get('vehicle_number', '').strip().upper()
        veh_type = request.form.get('vehicle_type', '').strip()
        brand = request.form.get('brand', '').strip()
        model = request.form.get('model', '').strip()
        rc_number = request.form.get('rc_number', '').strip().upper()
        rc_exp_str = request.form.get('rc_expiry_date', '').strip()
        insurance_num = request.form.get('insurance_number', '').strip()
        ins_exp_str = request.form.get('insurance_expiry_date', '').strip()
        capacity = request.form.get('capacity', '').strip()
        chassis_number = request.form.get('chassis_number', '').strip().upper()
        engine_number = request.form.get('engine_number', '').strip().upper()
        reg_date_str = request.form.get('registration_date', '').strip()
        assigned_driver_id_str = request.form.get('assigned_driver_id', '').strip()
        status = request.form.get('status', 'Active').strip()

        if not veh_num or not rc_number or not veh_type:
            flash("Vehicle Number, Vehicle Type, and RC Number are required.", "warning")
            return render_template('admin/vehicle_form.html', action="Add", vehicle=None, drivers=drivers)

        if Vehicle.query.filter_by(vehicle_number=veh_num).first():
            flash(f"Vehicle with number '{veh_num}' already exists in fleet.", "danger")
            return render_template('admin/vehicle_form.html', action="Add", vehicle=None, drivers=drivers)

        if Vehicle.query.filter_by(rc_number=rc_number).first():
            flash(f"Vehicle with RC Number '{rc_number}' is already registered.", "danger")
            return render_template('admin/vehicle_form.html', action="Add", vehicle=None, drivers=drivers)

        assigned_driver_id = int(assigned_driver_id_str) if assigned_driver_id_str.isdigit() else None

        v = Vehicle(
            vehicle_number=veh_num,
            vehicle_type=veh_type,
            brand=brand,
            model=model,
            rc_number=rc_number,
            insurance_number=insurance_num,
            capacity=capacity,
            chassis_number=chassis_number,
            engine_number=engine_number,
            assigned_driver_id=assigned_driver_id,
            status=status
        )

        if rc_exp_str:
            try:
                v.rc_expiry_date = datetime.strptime(rc_exp_str, '%Y-%m-%d').date()
            except ValueError:
                pass

        if ins_exp_str:
            try:
                v.insurance_expiry_date = datetime.strptime(ins_exp_str, '%Y-%m-%d').date()
            except ValueError:
                pass

        if reg_date_str:
            try:
                v.registration_date = datetime.strptime(reg_date_str, '%Y-%m-%d').date()
            except ValueError:
                pass

        db.session.add(v)
        db.session.commit()

        # Log Activity
        try:
            log = ActivityLog(
                user_id=session.get('user_id'),
                user_role='Admin',
                action='ADD_VEHICLE',
                description=f"Added new vehicle {veh_num} ({brand} {model}, {veh_type})"
            )
            db.session.add(log)
            db.session.commit()
        except Exception:
            pass

        flash(f"Vehicle {veh_num} successfully registered to fleet.", "success")
        return redirect(url_for('admin.vehicle_details', vehicle_id=v.id))

    return render_template('admin/vehicle_form.html', action="Add", vehicle=None, drivers=drivers)

@admin_bp.route('/vehicles/<int:vehicle_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_vehicle(vehicle_id):
    vehicle = Vehicle.query.get_or_404(vehicle_id)
    drivers = Driver.query.filter_by(status='Active').order_by(Driver.full_name).all()

    if request.method == 'POST':
        veh_num = request.form.get('vehicle_number', vehicle.vehicle_number).strip().upper()
        rc_number = request.form.get('rc_number', vehicle.rc_number).strip().upper()

        # Check unique constraints if changed
        existing_v = Vehicle.query.filter(Vehicle.vehicle_number == veh_num, Vehicle.id != vehicle.id).first()
        if existing_v:
            flash(f"Vehicle number '{veh_num}' is already used by another truck.", "danger")
            return render_template('admin/vehicle_form.html', action="Edit", vehicle=vehicle, drivers=drivers)

        existing_rc = Vehicle.query.filter(Vehicle.rc_number == rc_number, Vehicle.id != vehicle.id).first()
        if existing_rc:
            flash(f"RC number '{rc_number}' is already registered to another vehicle.", "danger")
            return render_template('admin/vehicle_form.html', action="Edit", vehicle=vehicle, drivers=drivers)

        vehicle.vehicle_number = veh_num
        vehicle.vehicle_type = request.form.get('vehicle_type', vehicle.vehicle_type).strip()
        vehicle.brand = request.form.get('brand', vehicle.brand).strip()
        vehicle.model = request.form.get('model', vehicle.model).strip()
        vehicle.rc_number = rc_number
        vehicle.insurance_number = request.form.get('insurance_number', vehicle.insurance_number).strip()
        vehicle.capacity = request.form.get('capacity', vehicle.capacity).strip()
        vehicle.chassis_number = request.form.get('chassis_number', vehicle.chassis_number).strip().upper()
        vehicle.engine_number = request.form.get('engine_number', vehicle.engine_number).strip().upper()
        vehicle.status = request.form.get('status', vehicle.status).strip()

        assigned_driver_id_str = request.form.get('assigned_driver_id', '').strip()
        vehicle.assigned_driver_id = int(assigned_driver_id_str) if assigned_driver_id_str.isdigit() else None

        rc_exp_str = request.form.get('rc_expiry_date', '').strip()
        if rc_exp_str:
            try:
                vehicle.rc_expiry_date = datetime.strptime(rc_exp_str, '%Y-%m-%d').date()
            except ValueError:
                pass
        elif 'rc_expiry_date' in request.form and not rc_exp_str:
            vehicle.rc_expiry_date = None

        ins_exp_str = request.form.get('insurance_expiry_date', '').strip()
        if ins_exp_str:
            try:
                vehicle.insurance_expiry_date = datetime.strptime(ins_exp_str, '%Y-%m-%d').date()
            except ValueError:
                pass
        elif 'insurance_expiry_date' in request.form and not ins_exp_str:
            vehicle.insurance_expiry_date = None

        reg_date_str = request.form.get('registration_date', '').strip()
        if reg_date_str:
            try:
                vehicle.registration_date = datetime.strptime(reg_date_str, '%Y-%m-%d').date()
            except ValueError:
                pass
        elif 'registration_date' in request.form and not reg_date_str:
            vehicle.registration_date = None

        db.session.commit()

        try:
            log = ActivityLog(
                user_id=session.get('user_id'),
                user_role='Admin',
                action='EDIT_VEHICLE',
                description=f"Updated details for vehicle {vehicle.vehicle_number}"
            )
            db.session.add(log)
            db.session.commit()
        except Exception:
            pass

        flash(f"Vehicle {vehicle.vehicle_number} updated successfully.", "success")
        return redirect(url_for('admin.vehicle_details', vehicle_id=vehicle.id))

    return render_template('admin/vehicle_form.html', action="Edit", vehicle=vehicle, drivers=drivers)

@admin_bp.route('/vehicles/<int:vehicle_id>/details')
@admin_required
def vehicle_details(vehicle_id):
    vehicle = Vehicle.query.get_or_404(vehicle_id)
    memos = Memo.query.filter_by(vehicle_id=vehicle.id).order_by(Memo.memo_date.desc()).all()
    fuel_bills = FuelBill.query.filter_by(vehicle_id=vehicle.id).order_by(FuelBill.bill_date.desc()).all()
    drivers = Driver.query.filter_by(status='Active').order_by(Driver.full_name).all()
    all_vehicles = Vehicle.query.order_by(Vehicle.vehicle_number).all()

    total_revenue = sum(m.freight_amount for m in memos)
    total_expense = sum(m.total_expense for m in memos)
    total_profit = sum(m.profit for m in memos)
    
    # Expense Breakdown
    diesel_total = sum(m.expense.diesel_expense for m in memos if m.expense)
    toll_total = sum(m.expense.toll_expense for m in memos if m.expense)
    food_total = sum(m.expense.food_expense for m in memos if m.expense)
    loading_total = sum(m.expense.loading_charges for m in memos if m.expense)
    unloading_total = sum(m.expense.unloading_charges for m in memos if m.expense)
    other_total = sum(m.expense.other_expenses for m in memos if m.expense)
    total_fuel_bills_amount = sum(f.total_amount for f in fuel_bills)

    today = date.today()

    return render_template(
        'admin/vehicle_details.html',
        vehicle=vehicle,
        memos=memos,
        fuel_bills=fuel_bills,
        drivers=drivers,
        all_vehicles=all_vehicles,
        total_revenue=total_revenue,
        total_expense=total_expense,
        total_profit=total_profit,
        diesel_total=diesel_total,
        toll_total=toll_total,
        food_total=food_total,
        loading_total=loading_total,
        unloading_total=unloading_total,
        other_total=other_total,
        total_fuel_bills_amount=total_fuel_bills_amount,
        today=today
    )

@admin_bp.route('/vehicles/<int:vehicle_id>/renew-insurance', methods=['POST'])
@admin_required
def renew_vehicle_insurance(vehicle_id):
    vehicle = Vehicle.query.get_or_404(vehicle_id)
    new_policy = request.form.get('insurance_number', '').strip()
    new_exp_str = request.form.get('insurance_expiry_date', '').strip()

    if not new_exp_str:
        flash("Insurance Expiry Date is required for renewal.", "warning")
        return redirect(url_for('admin.vehicle_details', vehicle_id=vehicle.id))

    if new_policy:
        vehicle.insurance_number = new_policy

    try:
        vehicle.insurance_expiry_date = datetime.strptime(new_exp_str, '%Y-%m-%d').date()
        db.session.commit()
        flash(f"Insurance for vehicle {vehicle.vehicle_number} successfully renewed until {vehicle.insurance_expiry_date}.", "success")
    except ValueError:
        flash("Invalid date format for insurance expiry.", "danger")

    return redirect(url_for('admin.vehicle_details', vehicle_id=vehicle.id))

@admin_bp.route('/vehicles/<int:vehicle_id>/update-status', methods=['POST'])
@admin_required
def update_vehicle_status(vehicle_id):
    vehicle = Vehicle.query.get_or_404(vehicle_id)
    new_status = request.form.get('status', '').strip()
    valid_statuses = ['Active', 'In Maintenance', 'In Trip', 'Inactive']

    if new_status in valid_statuses:
        old_status = vehicle.status
        vehicle.status = new_status
        db.session.commit()
        flash(f"Vehicle {vehicle.vehicle_number} status changed from {old_status} to {new_status}.", "info")
    else:
        flash("Invalid vehicle status provided.", "warning")

    return redirect(request.referrer or url_for('admin.vehicle_details', vehicle_id=vehicle.id))

@admin_bp.route('/vehicles/<int:vehicle_id>/assign-driver', methods=['POST'])
@admin_required
def assign_vehicle_driver(vehicle_id):
    vehicle = Vehicle.query.get_or_404(vehicle_id)
    driver_id_str = request.form.get('driver_id', '').strip()
    if driver_id_str == 'none' or not driver_id_str:
        vehicle.assigned_driver_id = None
        db.session.commit()
        flash(f"Driver unassigned from vehicle {vehicle.vehicle_number}.", "info")
    elif driver_id_str.isdigit():
        driver = Driver.query.get_or_404(int(driver_id_str))
        vehicle.assigned_driver_id = driver.id
        db.session.commit()
        flash(f"Driver {driver.full_name} ({driver.driver_code}) successfully assigned to vehicle {vehicle.vehicle_number}.", "success")
    return redirect(request.referrer or url_for('admin.vehicle_details', vehicle_id=vehicle.id))

@admin_bp.route('/vehicles/<int:vehicle_id>/delete', methods=['POST'])
@admin_required
def delete_vehicle(vehicle_id):
    vehicle = Vehicle.query.get_or_404(vehicle_id)
    num = vehicle.vehicle_number

    # Safely detach associated memos and fuel bills so integrity is preserved
    for m in vehicle.memos:
        m.vehicle_id = None
    for f in vehicle.fuel_bills:
        f.vehicle_id = None

    db.session.delete(vehicle)
    db.session.commit()

    try:
        log = ActivityLog(
            user_id=session.get('user_id'),
            user_role='Admin',
            action='DELETE_VEHICLE',
            description=f"Permanently deleted vehicle {num} record"
        )
        db.session.add(log)
        db.session.commit()
    except Exception:
        pass

    flash(f"Vehicle {num} and its record have been permanently removed.", "info")
    return redirect(url_for('admin.vehicles'))

# ----------------- MEMO MAINTENANCE & ARCHIVE -----------------
@admin_bp.route('/memos')
@admin_required
def memos():
    search = request.args.get('q', '').strip()
    status = request.args.get('status', '').strip()
    start_date = request.args.get('start_date', '').strip()
    end_date = request.args.get('end_date', '').strip()

    memo_query = Memo.query
    if search:
        memo_query = memo_query.filter(
            (Memo.memo_number.ilike(f"%{search}%")) |
            (Memo.source.ilike(f"%{search}%")) |
            (Memo.destination.ilike(f"%{search}%")) |
            (Memo.vehicle_number_text.ilike(f"%{search}%"))
        )
    if status:
        memo_query = memo_query.filter_by(status=status)
    if start_date:
        try:
            s_d = datetime.strptime(start_date, '%Y-%m-%d').date()
            memo_query = memo_query.filter(Memo.memo_date >= s_d)
        except ValueError:
            pass
    if end_date:
        try:
            e_d = datetime.strptime(end_date, '%Y-%m-%d').date()
            memo_query = memo_query.filter(Memo.memo_date <= e_d)
        except ValueError:
            pass

    memo_list = memo_query.order_by(Memo.memo_date.desc()).all()
    
    total_rev = sum(m.freight_amount for m in memo_list)
    total_exp = sum(m.total_expense for m in memo_list)
    total_prof = sum(m.profit for m in memo_list)

    return render_template(
        'admin/memos.html',
        memos=memo_list,
        search=search,
        status=status,
        start_date=start_date,
        end_date=end_date,
        total_rev=total_rev,
        total_exp=total_exp,
        total_prof=total_prof
    )

@admin_bp.route('/memos/<int:memo_id>')
@admin_required
def memo_detail(memo_id):
    memo = Memo.query.get_or_404(memo_id)
    fuel_bills = FuelBill.query.filter_by(memo_id=memo.id).all()
    fuel_analysis = analyze_fuel_consumption(memo, memo.vehicle, fuel_bills)
    return render_template('admin/memo_detail.html', memo=memo, fuel_bills=fuel_bills, fuel_analysis=fuel_analysis)

@admin_bp.route('/memos/<int:memo_id>/export_excel')
@admin_required
def export_memo_excel(memo_id):
    import json
    from services.memo_table_service import MemoTableExtractor

    memo = Memo.query.get_or_404(memo_id)
    exp = memo.expense
    diesel = exp.diesel_expense if exp else 0.0
    toll = exp.toll_expense if exp else 0.0
    food = exp.food_expense if exp else 0.0
    loading = exp.loading_charges if exp else 0.0
    unloading = exp.unloading_charges if exp else 0.0
    other = exp.other_expenses if exp else 0.0
    commission = 0.0

    table_rows = []
    if memo.extracted_json:
        try:
            ej = json.loads(memo.extracted_json)
            table_rows = ej.get("table_rows", [])
            commission = float(ej.get("commission_expense") or 0.0)
            if not commission and "financial_summary" in ej:
                commission = float(ej["financial_summary"].get("commission_expense") or 0.0)
        except Exception:
            table_rows = []

    if not table_rows:
        table_rows = [
            {"s_no": 1, "category_name_en": "Agreed Freight", "category_name_ta": "லாரி வாடகை", "detected_text": "Agreed Freight", "amount": memo.freight_amount, "is_expense": False},
            {"s_no": 2, "category_name_en": "Advance Paid", "category_name_ta": "முன்பணம்", "detected_text": "Advance", "amount": memo.advance_amount, "is_expense": False},
            {"s_no": 3, "category_name_en": "Diesel / Fuel", "category_name_ta": "டீசல் செலவு", "detected_text": "Diesel", "amount": diesel, "is_expense": True},
            {"s_no": 4, "category_name_en": "Toll / Fastag", "category_name_ta": "சுங்கம் / டோல்கேட்", "detected_text": "Toll", "amount": toll, "is_expense": True},
            {"s_no": 5, "category_name_en": "Driver Food & Bata", "category_name_ta": "படி / சாப்பாடு", "detected_text": "Food", "amount": food, "is_expense": True},
            {"s_no": 6, "category_name_en": "Loading Charges", "category_name_ta": "ஏற்று கூலி", "detected_text": "Loading", "amount": loading, "is_expense": True},
            {"s_no": 7, "category_name_en": "Unloading Charges", "category_name_ta": "இறக்கு கூலி", "detected_text": "Unloading", "amount": unloading, "is_expense": True},
            {"s_no": 8, "category_name_en": "Broker / Commission", "category_name_ta": "கமிஷன் செலவு", "detected_text": "Commission", "amount": commission, "is_expense": True},
            {"s_no": 9, "category_name_en": "Other Expenses", "category_name_ta": "இதர செலவு", "detected_text": exp.other_notes or "Misc", "amount": other, "is_expense": True}
        ]
        table_rows = [r for r in table_rows if r["amount"] > 0 or r["category_name_en"] in ["Agreed Freight", "Advance Paid", "Diesel / Fuel"]]
        for idx, r in enumerate(table_rows):
            r["s_no"] = idx + 1

    memo_meta = {
        "memo_number": memo.memo_number,
        "memo_date": str(memo.memo_date),
        "vehicle_number": memo.vehicle_number_text or (memo.vehicle.vehicle_number if memo.vehicle else "N/A"),
        "driver_name": memo.driver.full_name if memo.driver else "N/A",
        "driver_phone": memo.driver_phone or (memo.driver.phone if memo.driver else "N/A"),
        "customer_name": memo.customer.company_name if memo.customer else "Direct Booking",
        "source": memo.source,
        "destination": memo.destination,
        "material": memo.material
    }
    financial_summary = {
        "freight_amount": memo.freight_amount,
        "advance_amount": memo.advance_amount,
        "total_expense": memo.total_expense,
        "diesel_expense": diesel,
        "toll_expense": toll,
        "food_expense": food,
        "loading_charges": loading,
        "unloading_charges": unloading,
        "commission_expense": commission,
        "other_expenses": other,
        "net_profit": memo.profit,
        "driver_balance": memo.net_amount
    }
    excel_buf = MemoTableExtractor.generate_excel_workbook(memo_meta, table_rows, financial_summary)
    filename = f"Admin_Memo_{memo.memo_number}_{memo.memo_date}.xlsx"
    return send_file(
        excel_buf,
        as_attachment=True,
        download_name=filename,
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

# ----------------- FUEL MONITORING & THEFT DETECTION -----------------
@admin_bp.route('/fuel-monitoring')
@admin_required
def fuel_monitoring():
    all_memos = Memo.query.order_by(Memo.memo_date.desc()).all()
    theft_records = []

    for m in all_memos:
        fbs = FuelBill.query.filter_by(memo_id=m.id).all()
        analysis = analyze_fuel_consumption(m, m.vehicle, fbs)
        driver_name = m.driver.full_name if m.driver else "Unknown"
        veh_num = m.vehicle.vehicle_number if m.vehicle else (m.vehicle_number_text or "N/A")
        analysis["driver_name"] = driver_name
        analysis["vehicle_number"] = veh_num
        analysis["memo_date"] = m.memo_date
        theft_records.append(analysis)

    high_risk_count = sum(1 for r in theft_records if r["risk_level"] == "High Risk")
    warning_count = sum(1 for r in theft_records if r["risk_level"] == "Warning")
    normal_count = sum(1 for r in theft_records if r["risk_level"] == "Normal")

    return render_template(
        'admin/fuel_monitoring.html',
        records=theft_records,
        high_risk_count=high_risk_count,
        warning_count=warning_count,
        normal_count=normal_count
    )

# ----------------- NOTIFICATIONS -----------------
@admin_bp.route('/notifications')
@admin_required
def notifications():
    notif_list = Notification.query.order_by(Notification.id.desc()).all()
    return render_template('admin/notifications.html', notifications=notif_list)

@admin_bp.route('/notifications/<int:notif_id>/mark-read', methods=['POST'])
@admin_required
def mark_notification_read(notif_id):
    notif = Notification.query.get_or_404(notif_id)
    notif.is_read = True
    db.session.commit()
    return jsonify({"success": True})

@admin_bp.route('/notifications/mark-all-read', methods=['POST'])
@admin_required
def mark_all_read():
    Notification.query.update({"is_read": True})
    db.session.commit()
    flash("All notifications marked as read.", "info")
    return redirect(url_for('admin.notifications'))

# ----------------- REPORT GENERATION -----------------
@admin_bp.route('/reports')
@admin_required
def reports():
    return render_template('admin/reports.html')

@admin_bp.route('/reports/export/<format_type>')
@admin_required
def export_report(format_type):
    report_type = request.args.get('type', 'memo').lower() # memo, expense, profit, vehicle, driver, fuel
    
    headers = []
    rows = []
    summary = {}
    title = ""

    if report_type == 'memo':
        title = "Trip Memos & Profitability Summary"
        headers = ["Memo #", "Date", "Vehicle", "Driver", "Route", "Freight (Rs)", "Expense (Rs)", "Profit (Rs)", "Status"]
        memos = Memo.query.order_by(Memo.memo_date.desc()).all()
        for m in memos:
            d_name = m.driver.full_name if m.driver else ""
            v_no = m.vehicle.vehicle_number if m.vehicle else (m.vehicle_number_text or "")
            rows.append([
                m.memo_number,
                m.memo_date.strftime('%d-%m-%Y'),
                v_no,
                d_name,
                f"{m.source} -> {m.destination}",
                f"{m.freight_amount:,.2f}",
                f"{m.total_expense:,.2f}",
                f"{m.profit:,.2f}",
                m.status
            ])
        summary = {
            "Total Trips Logged": len(memos),
            "Total Freight Revenue": f"Rs. {sum(m.freight_amount for m in memos):,.2f}",
            "Total Operating Expenses": f"Rs. {sum(m.total_expense for m in memos):,.2f}",
            "Net Fleet Profit": f"Rs. {sum(m.profit for m in memos):,.2f}"
        }

    elif report_type == 'expense':
        title = "Fleet Operating Expense Breakdown"
        headers = ["Memo #", "Vehicle", "Diesel (Rs)", "Tolls (Rs)", "Driver Food (Rs)", "Loading (Rs)", "Unloading (Rs)", "Other (Rs)", "Total Expense"]
        memos = Memo.query.order_by(Memo.memo_date.desc()).all()
        tot_diesel = tot_toll = tot_food = tot_loading = tot_unloading = tot_other = 0.0
        for m in memos:
            exp = m.expense
            v_no = m.vehicle.vehicle_number if m.vehicle else (m.vehicle_number_text or "")
            d = exp.diesel_expense if exp else 0.0
            t = exp.toll_expense if exp else 0.0
            f = exp.food_expense if exp else 0.0
            l = exp.loading_charges if exp else 0.0
            u = exp.unloading_charges if exp else 0.0
            o = exp.other_expenses if exp else 0.0
            tot_diesel += d; tot_toll += t; tot_food += f; tot_loading += l; tot_unloading += u; tot_other += o
            rows.append([
                m.memo_number,
                v_no,
                f"{d:,.2f}", f"{t:,.2f}", f"{f:,.2f}", f"{l:,.2f}", f"{u:,.2f}", f"{o:,.2f}",
                f"{m.total_expense:,.2f}"
            ])
        summary = {
            "Total Diesel Cost": f"Rs. {tot_diesel:,.2f}",
            "Total Tolls Paid": f"Rs. {tot_toll:,.2f}",
            "Driver Food & Allowance": f"Rs. {tot_food:,.2f}",
            "Loading & Unloading Charges": f"Rs. {(tot_loading + tot_unloading):,.2f}",
            "Total Fleet Expenses": f"Rs. {sum(m.total_expense for m in memos):,.2f}"
        }

    elif report_type == 'vehicle':
        title = "Vehicle Performance & Compliance Report"
        headers = ["Vehicle #", "Type", "Model", "Capacity", "RC Number", "Insurance Expiry", "Trips", "Revenue (Rs)", "Profit (Rs)"]
        vehicles = Vehicle.query.all()
        for v in vehicles:
            v_memos = Memo.query.filter_by(vehicle_id=v.id).all()
            v_rev = sum(m.freight_amount for m in v_memos)
            v_prof = sum(m.profit for m in v_memos)
            exp_str = v.insurance_expiry_date.strftime('%d-%m-%Y') if v.insurance_expiry_date else "N/A"
            rows.append([
                v.vehicle_number,
                v.vehicle_type,
                v.model or "Standard",
                v.capacity or "N/A",
                v.rc_number,
                exp_str,
                len(v_memos),
                f"{v_rev:,.2f}",
                f"{v_prof:,.2f}"
            ])
        summary = {
            "Active Fleet Vehicles": len(vehicles),
            "Total Completed Trips": Memo.query.count()
        }

    elif report_type == 'driver':
        title = "Driver Performance & Trip Operations Report"
        headers = ["Code", "Driver Name", "Phone", "License #", "Status", "Trips", "Revenue Generated (Rs)", "Customers"]
        drivers = Driver.query.all()
        for d in drivers:
            d_memos = Memo.query.filter_by(driver_id=d.id).all()
            d_custs = Customer.query.filter_by(driver_id=d.id).count()
            d_rev = sum(m.freight_amount for m in d_memos)
            rows.append([
                d.driver_code,
                d.full_name,
                d.phone,
                d.license_number,
                d.status,
                len(d_memos),
                f"{d_rev:,.2f}",
                d_custs
            ])
        summary = {
            "Total Registered Drivers": len(drivers)
        }

    elif report_type == 'fuel':
        title = "Fuel Consumption & Pilferage Monitoring Report"
        headers = ["Trip #", "Route", "Vehicle", "Driver", "Est. Liters", "Actual Liters", "Variance (L)", "% Variance", "Risk Level"]
        memos = Memo.query.all()
        for m in memos:
            analysis = analyze_fuel_consumption(m, m.vehicle)
            rows.append([
                m.memo_number,
                f"{m.source} -> {m.destination}",
                m.vehicle.vehicle_number if m.vehicle else (m.vehicle_number_text or ""),
                m.driver.full_name if m.driver else "",
                f"{analysis['expected_liters']} L",
                f"{analysis['actual_liters']} L",
                f"{analysis['diff_liters']} L",
                f"{analysis['pct_diff']}%",
                analysis["risk_level"]
            ])
        summary = {
            "Audited Trips": len(memos),
            "Fuel Anomaly Incidents": sum(1 for m in memos if analyze_fuel_consumption(m, m.vehicle)["is_suspicious"])
        }

    else:
        # Default to memo
        return redirect(url_for('admin.export_report', format_type=format_type, type='memo'))

    timestamp = datetime.now().strftime('%Y%m%d_%H%M')
    if format_type.lower() == 'pdf':
        if not generate_pdf_report:
            flash("Report export is currently disabled.", "warning")
            return redirect(url_for('admin.reports'))
        pdf_stream = generate_pdf_report(report_type, title, headers, rows, summary)
        return send_file(
            pdf_stream,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=f"{report_type}_report_{timestamp}.pdf"
        )
    elif format_type.lower() == 'docx':
        if not generate_docx_report:
            flash("Report export is currently disabled.", "warning")
            return redirect(url_for('admin.reports'))
        docx_stream = generate_docx_report(report_type, title, headers, rows, summary)
        return send_file(
            docx_stream,
            mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            as_attachment=True,
            download_name=f"{report_type}_report_{timestamp}.docx"
        )
    else:
        flash("Invalid report format requested.", "danger")
        return redirect(url_for('admin.reports'))
