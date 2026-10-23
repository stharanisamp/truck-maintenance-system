import os
from datetime import date, timedelta
from models import db, Admin, Driver, Vehicle, Customer, Memo, MemoExpense, FuelBill, Notification, ActivityLog
from config import Config

def init_upload_folders():
    for folder in [
        Config.UPLOAD_FOLDER,
        Config.MEMO_UPLOAD_FOLDER,
        Config.FUEL_UPLOAD_FOLDER,
        Config.PROFILE_UPLOAD_FOLDER,
        os.path.join(Config.BASE_DIR, "static", "sample_memos")
    ]:
        try:
            os.makedirs(folder, exist_ok=True)
        except OSError:
            pass

def seed_initial_data(app):
    with app.app_context():
        # 1. Admin account
        admin = Admin.query.first()
        if not admin:
            admin = Admin(
                username="admin",
                email="stharanisamp@gmail.com",
                full_name="Tharani (Fleet Owner)",
                phone="+91 98765 43210"
            )
            admin.set_password("admin123")
            db.session.add(admin)
            db.session.commit()
            print("[Database] Created default Admin: stharanisamp@gmail.com / admin123")

        # 2. Seed Sample Vehicles
        # 2. Seed Sample Vehicles
        if Vehicle.query.count() == 0:
            vehicles = [
                Vehicle(
                    vehicle_number="TN 28 AB 1234",
                    vehicle_type="10 Wheeler",
                    brand="Tata Motors",
                    model="Signa 2823.K",
                    rc_number="RC-TN28-2021-9988",
                    rc_expiry_date=date.today() + timedelta(days=3650),
                    insurance_number="INS-HDFC-88990",
                    insurance_expiry_date=date.today() + timedelta(days=240),
                    capacity="28 Tons",
                    chassis_number="MAT624001E0A12345",
                    engine_number="6TC98765432",
                    registration_date=date(2021, 3, 12),
                    assigned_driver_id=1,
                    status="Active"
                ),
                Vehicle(
                    vehicle_number="TN 30 CD 5678",
                    vehicle_type="14 Wheeler",
                    brand="Ashok Leyland",
                    model="3520 Multi-Axle",
                    rc_number="RC-TN30-2022-7711",
                    rc_expiry_date=date.today() + timedelta(days=4000),
                    insurance_number="INS-ICICI-44332",
                    insurance_expiry_date=date.today() + timedelta(days=15), # Near expiry alert test
                    capacity="35 Tons",
                    chassis_number="MB1A12345F0B56789",
                    engine_number="H6ETIC4RU22",
                    registration_date=date(2022, 5, 18),
                    assigned_driver_id=2,
                    status="In Trip"
                ),
                Vehicle(
                    vehicle_number="TN 52 EF 9012",
                    vehicle_type="Container",
                    brand="BharatBenz",
                    model="2823R Heavy Truck",
                    rc_number="RC-TN52-2023-3344",
                    rc_expiry_date=date.today() + timedelta(days=4500),
                    insurance_number="INS-BAJAJ-11223",
                    insurance_expiry_date=date.today() + timedelta(days=320),
                    capacity="30 Tons",
                    chassis_number="ME1B98765G0C90123",
                    engine_number="OM926LA110",
                    registration_date=date(2023, 9, 10),
                    assigned_driver_id=3,
                    status="Active"
                ),
                Vehicle(
                    vehicle_number="TN 88 GH 3456",
                    vehicle_type="Trailer",
                    brand="Eicher Motors",
                    model="Pro 6040 Trailer",
                    rc_number="RC-TN88-2020-5566",
                    rc_expiry_date=date.today() + timedelta(days=3200),
                    insurance_number="INS-TATA-66778",
                    insurance_expiry_date=date.today() - timedelta(days=5), # Expired alert test
                    capacity="40 Tons",
                    chassis_number="MC2C54321H0D34567",
                    engine_number="VEDX8CRDI04",
                    registration_date=date(2020, 11, 25),
                    assigned_driver_id=4,
                    status="In Maintenance"
                )
            ]
            db.session.add_all(vehicles)
            db.session.commit()
            print("[Database] Seeded 4 sample vehicles.")
        else:
            # Backfill existing records if brand is empty
            v_backfill = {
                "TN 28 AB 1234": ("Tata Motors", "Signa 2823.K", "MAT624001E0A12345", "6TC98765432", date(2021, 3, 12), date(2036, 3, 12), 1, "Active"),
                "TN 30 CD 5678": ("Ashok Leyland", "3520 Multi-Axle", "MB1A12345F0B56789", "H6ETIC4RU22", date(2022, 5, 18), date(2037, 5, 18), 2, "In Trip"),
                "TN 52 EF 9012": ("BharatBenz", "2823R Heavy Truck", "ME1B98765G0C90123", "OM926LA110", date(2023, 9, 10), date(2038, 9, 10), 3, "Active"),
                "TN 88 GH 3456": ("Eicher Motors", "Pro 6040 Trailer", "MC2C54321H0D34567", "VEDX8CRDI04", date(2020, 11, 25), date(2035, 11, 25), 4, "In Maintenance"),
            }
            changed = False
            for v in Vehicle.query.all():
                if not getattr(v, 'brand', None):
                    info = v_backfill.get(v.vehicle_number)
                    if info:
                        v.brand, v.model, v.chassis_number, v.engine_number, v.registration_date, v.rc_expiry_date, v.assigned_driver_id, v.status = info
                    else:
                        v.brand = "Ashok Leyland"
                        v.chassis_number = f"CHAS-{v.id:04d}-{v.vehicle_number[-4:]}"
                        v.engine_number = f"ENG-{v.id:04d}-{v.vehicle_number[-4:]}"
                        v.registration_date = date.today() - timedelta(days=365)
                        v.rc_expiry_date = date.today() + timedelta(days=3650)
                        if not v.status or v.status == 'Maintenance':
                            v.status = 'In Maintenance'
                    changed = True
            if changed:
                try:
                    db.session.commit()
                    print("[Database] Backfilled complete vehicle information.")
                except Exception as ex:
                    db.session.rollback()
                    print(f"[Database] Backfill notice: {ex}")

        # 3. Seed Sample Drivers
        if Driver.query.count() == 0:
            drivers = [
                Driver(
                    driver_code="DRV-001",
                    full_name="Murugan Selvam",
                    email="murugan@truck.com",
                    phone="+91 94431 11223",
                    address="42 Anna Nagar, Namakkal, Tamil Nadu",
                    license_number="TN-28-2015-001122",
                    license_expiry_date=date.today() + timedelta(days=500),
                    date_of_birth=date(1986, 5, 14),
                    joining_date=date(2021, 1, 10),
                    status="Active"
                ),
                Driver(
                    driver_code="DRV-002",
                    full_name="Karthik Pandian",
                    email="karthik@truck.com",
                    phone="+91 98840 22334",
                    address="18 Bypass Road, Sankari, Salem, Tamil Nadu",
                    license_number="TN-30-2018-004455",
                    license_expiry_date=date.today() + timedelta(days=20), # Near expiry test
                    date_of_birth=date(1991, 10, 22),
                    joining_date=date(2022, 3, 15),
                    status="Active"
                ),
                Driver(
                    driver_code="DRV-003",
                    full_name="Ramesh Kumar",
                    email="ramesh@truck.com",
                    phone="+91 97722 33445",
                    address="89 NH-44 Tiruchengode, Tamil Nadu",
                    license_number="TN-52-2016-009988",
                    license_expiry_date=date.today() + timedelta(days=360),
                    date_of_birth=date(1989, 2, 18),
                    joining_date=date(2023, 6, 1),
                    status="Active"
                )
            ]
            for d in drivers:
                d.set_password("driver123")
                db.session.add(d)
            db.session.commit()
            print("[Database] Seeded 3 sample drivers (password: driver123).")

        # 4. Seed Sample Customers for Driver 1 & Driver 2
        d1 = Driver.query.filter_by(driver_code="DRV-001").first()
        d2 = Driver.query.filter_by(driver_code="DRV-002").first()
        v1 = Vehicle.query.filter_by(vehicle_number="TN 28 AB 1234").first()
        v2 = Vehicle.query.filter_by(vehicle_number="TN 30 CD 5678").first()

        if Customer.query.count() == 0 and d1:
            customers = [
                Customer(
                    driver_id=d1.id,
                    company_name="Annamalai Cement Logistics",
                    contact_person="V. Senthil Nathan",
                    mobile_number="+91 98427 12345",
                    email="dispatch@annamalai.in",
                    address="Industrial Estate, Ariyalur",
                    gst_number="33AAACA1234A1Z5",
                    loading_location="Ariyalur Cement Plant",
                    unloading_location="Chennai Harbour Yard"
                ),
                Customer(
                    driver_id=d1.id,
                    company_name="Kongu Steel Traders",
                    contact_person="P. Arumugam",
                    mobile_number="+91 94422 67890",
                    email="kongusteels@yahoo.com",
                    address="Steel Market, Salem",
                    gst_number="33AABCK5678B1Z2",
                    loading_location="Salem Steel Plant",
                    unloading_location="Coimbatore SIDCO"
                ),
                Customer(
                    driver_id=d2.id if d2 else d1.id,
                    company_name="Cauvery Granites Ltd",
                    contact_person="K. Balan",
                    mobile_number="+91 97890 54321",
                    email="orders@cauverygranites.com",
                    address="SIPCOT Phase II, Hosur",
                    gst_number="33AAACG9012C1Z8",
                    loading_location="Hosur Quarry",
                    unloading_location="Tuticorin Port"
                )
            ]
            db.session.add_all(customers)
            db.session.commit()
            print("[Database] Seeded 3 sample customers.")

        # 5. Seed Sample Memos and Expenses
        if Memo.query.count() == 0 and d1 and v1:
            m1 = Memo(
                memo_number="MEMO-2026-001",
                driver_id=d1.id,
                vehicle_id=v1.id,
                vehicle_number_text=v1.vehicle_number,
                memo_date=date.today() - timedelta(days=12),
                source="Ariyalur",
                destination="Chennai Harbour",
                freight_amount=48000.0,
                advance_amount=15000.0,
                total_expense=32400.0,
                profit=15600.0,
                net_amount=600.0,
                status="Profit",
                memo_file_path="sample_memos/sample_memo_1.png"
            )
            db.session.add(m1)
            db.session.flush()

            exp1 = MemoExpense(
                memo_id=m1.id,
                diesel_expense=21500.0,
                toll_expense=3200.0,
                food_expense=2200.0,
                loading_charges=3000.0,
                unloading_charges=2000.0,
                other_expenses=500.0,
                other_notes="Puncture repair at Tindivanam"
            )
            db.session.add(exp1)

            # Memo 2
            m2 = Memo(
                memo_number="MEMO-2026-002",
                driver_id=d1.id,
                vehicle_id=v1.id,
                vehicle_number_text=v1.vehicle_number,
                memo_date=date.today() - timedelta(days=5),
                source="Salem",
                destination="Coimbatore",
                freight_amount=26000.0,
                advance_amount=8000.0,
                total_expense=18500.0,
                profit=7500.0,
                net_amount=-500.0,
                status="Profit",
                memo_file_path="sample_memos/sample_memo_2.png"
            )
            db.session.add(m2)
            db.session.flush()

            exp2 = MemoExpense(
                memo_id=m2.id,
                diesel_expense=12500.0,
                toll_expense=1600.0,
                food_expense=1400.0,
                loading_charges=1500.0,
                unloading_charges=1200.0,
                other_expenses=300.0,
                other_notes="Weighbridge slip"
            )
            db.session.add(exp2)

            # Memo 3 (Loss trip for testing)
            if v2 and d2:
                m3 = Memo(
                    memo_number="MEMO-2026-003",
                    driver_id=d2.id,
                    vehicle_id=v2.id,
                    vehicle_number_text=v2.vehicle_number,
                    memo_date=date.today() - timedelta(days=2),
                    source="Hosur",
                    destination="Tuticorin",
                    freight_amount=42000.0,
                    advance_amount=10000.0,
                    total_expense=45200.0,
                    profit=-3200.0,
                    net_amount=-13200.0,
                    status="Loss",
                    memo_file_path="sample_memos/sample_memo_3.png"
                )
                db.session.add(m3)
                db.session.flush()

                exp3 = MemoExpense(
                    memo_id=m3.id,
                    diesel_expense=31000.0,
                    toll_expense=4800.0,
                    food_expense=2800.0,
                    loading_charges=3200.0,
                    unloading_charges=2600.0,
                    other_expenses=800.0,
                    other_notes="Emergency radiator hose fix"
                )
                db.session.add(exp3)

            db.session.commit()
            print("[Database] Seeded sample memos and expense records.")

        # 6. Seed Sample Fuel Bills
        if FuelBill.query.count() == 0 and d1 and v1:
            fbills = [
                FuelBill(
                    driver_id=d1.id,
                    vehicle_id=v1.id,
                    memo_id=1,
                    fuel_station_name="Indian Oil Corporation - Tindivanam Bypass",
                    bill_number="IOCL-B7721",
                    bill_date=date.today() - timedelta(days=12),
                    fuel_quantity=180.0,
                    rate_per_liter=95.5,
                    total_amount=17190.0,
                    bill_file_path="sample_memos/sample_fuel_bill_1.png"
                ),
                FuelBill(
                    driver_id=d1.id,
                    vehicle_id=v1.id,
                    memo_id=1,
                    fuel_station_name="Bharat Petroleum - Chengalpattu",
                    bill_number="BPCL-99014",
                    bill_date=date.today() - timedelta(days=11),
                    fuel_quantity=45.0,
                    rate_per_liter=95.8,
                    total_amount=4311.0,
                    bill_file_path="sample_memos/sample_fuel_bill_2.png"
                ),
                FuelBill(
                    driver_id=d2.id if d2 else d1.id,
                    vehicle_id=v2.id if v2 else v1.id,
                    memo_id=3 if d2 and v2 else 2,
                    fuel_station_name="HPCL Oasis Express - Madurai Ring Road",
                    bill_number="HPCL-6652",
                    bill_date=date.today() - timedelta(days=2),
                    fuel_quantity=320.0, # High fuel consumption for anomaly test
                    rate_per_liter=96.0,
                    total_amount=30720.0,
                    bill_file_path="sample_memos/sample_fuel_bill_3.png"
                )
            ]
            db.session.add_all(fbills)
            db.session.commit()
            print("[Database] Seeded 3 sample fuel bills.")

        # 7. Seed Sample Notifications & Alerts
        if Notification.query.count() == 0:
            notifs = [
                Notification(
                    title="Suspicious Fuel Consumption Warning",
                    message="Vehicle TN 30 CD 5678 logged 320 Liters on Hosur to Tuticorin trip (Expected: 240 Liters). Discrepancy: +33.3% [High Risk].",
                    alert_type="FUEL_THEFT",
                    severity="High Risk",
                    is_read=False,
                    link="/admin/fuel-monitoring"
                ),
                Notification(
                    title="Vehicle Insurance Expiry Warning",
                    message="Vehicle TN 30 CD 5678 insurance expires in 15 days (Policy # INS-ICICI-44332).",
                    alert_type="INSURANCE_EXPIRY",
                    severity="Warning",
                    is_read=False,
                    link="/admin/vehicles"
                ),
                Notification(
                    title="Vehicle Insurance Expired Alert",
                    message="Vehicle TN 88 GH 3456 insurance expired 5 days ago! Immediate renewal required.",
                    alert_type="INSURANCE_EXPIRY",
                    severity="High Risk",
                    is_read=False,
                    link="/admin/vehicles"
                ),
                Notification(
                    title="Driver License Renewal Alert",
                    message="Driver Karthik Pandian's driving license expires in 20 days.",
                    alert_type="LICENSE_EXPIRY",
                    severity="Warning",
                    is_read=False,
                    link="/admin/drivers"
                ),
                Notification(
                    title="New Memo Uploaded",
                    message="Driver Murugan Selvam uploaded trip memo MEMO-2026-002 (Salem -> Coimbatore).",
                    alert_type="NEW_MEMO",
                    severity="Normal",
                    is_read=True,
                    link="/admin/memos"
                )
            ]
            db.session.add_all(notifs)
            db.session.commit()
            print("[Database] Seeded 5 initial system notifications.")

        # 8. Seed Initial Activity Logs
        if ActivityLog.query.count() == 0 and admin:
            logs = [
                ActivityLog(user_type="Admin", user_id=admin.id, user_name=admin.full_name, action="System Init", details="Initialized Truck Maintenance System with seed records"),
                ActivityLog(user_type="Driver", user_id=d1.id if d1 else 1, user_name="Murugan Selvam", action="Upload Memo", details="Uploaded MEMO-2026-001"),
                ActivityLog(user_type="Driver", user_id=d1.id if d1 else 1, user_name="Murugan Selvam", action="Upload Fuel Bill", details="Uploaded IOCL-B7721 (180 L)")
            ]
            db.session.add_all(logs)
            db.session.commit()

def migrate_memo_columns(app):
    """Safely adds new memo verification columns if they do not exist yet."""
    with app.app_context():
        try:
            from sqlalchemy import text
            columns_to_add = [
                ("enhanced_image_path", "VARCHAR(255)"),
                ("extracted_json", "TEXT"),
                ("verification_status", "VARCHAR(50) DEFAULT 'SAVED'"),
                ("confidence_score", "FLOAT DEFAULT 1.0"),
                ("material", "VARCHAR(150)"),
                ("load_quantity", "VARCHAR(50)"),
                ("start_km", "FLOAT"),
                ("end_km", "FLOAT"),
                ("driver_phone", "VARCHAR(50)")
            ]
            for col_name, col_type in columns_to_add:
                try:
                    db.session.execute(text(f"ALTER TABLE memos ADD COLUMN {col_name} {col_type};"))
                    db.session.commit()
                except Exception:
                    db.session.rollback()
        except Exception as e:
            print(f"[Database] Migration notice: {e}")

def migrate_vehicle_columns(app):
    """Safely adds new vehicle management columns if they do not exist yet."""
    with app.app_context():
        try:
            from sqlalchemy import text
            columns_to_add = [
                ("brand", "VARCHAR(100)"),
                ("rc_expiry_date", "DATE"),
                ("chassis_number", "VARCHAR(100)"),
                ("engine_number", "VARCHAR(100)"),
                ("registration_date", "DATE"),
                ("assigned_driver_id", "INTEGER")
            ]
            for col_name, col_type in columns_to_add:
                try:
                    db.session.execute(text(f"ALTER TABLE vehicles ADD COLUMN {col_name} {col_type};"))
                    db.session.commit()
                except Exception:
                    db.session.rollback()
        except Exception as e:
            print(f"[Database] Vehicle migration notice: {e}")

def ensure_mysql_database_exists(app):
    """If using MySQL and the target database does not exist, auto-create it."""
    uri = app.config.get("SQLALCHEMY_DATABASE_URI", "")
    if uri.startswith("mysql"):
        try:
            from sqlalchemy.engine.url import make_url
            import pymysql
            parsed = make_url(uri)
            db_name = parsed.database
            if db_name:
                conn = pymysql.connect(
                    host=parsed.host or '127.0.0.1',
                    port=parsed.port or 3306,
                    user=parsed.username or 'root',
                    password=parsed.password or '',
                    charset='utf8mb4'
                )
                with conn.cursor() as cur:
                    cur.execute(f"CREATE DATABASE IF NOT EXISTS `{db_name}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
                conn.commit()
                conn.close()
                print(f"[Database] MySQL database '{db_name}' verified/ready.")
        except Exception as e:
            print(f"[Database] Note: Could not auto-create MySQL database (may already exist or requires permissions): {e}")

def init_db(app):
    init_upload_folders()
    ensure_mysql_database_exists(app)
    with app.app_context():
        try:
            db.create_all()
            migrate_memo_columns(app)
            migrate_vehicle_columns(app)
            seed_initial_data(app)
        except Exception as e:
            print(f"[Database Warning] Could not connect to configured database: {e}")
            print("[Database Fallback] Falling back to local offline SQLite database...")
            try:
                from config import BASE_DIR, Config
                sqlite_path = "/tmp/truck_maintenance_system.db" if getattr(Config, 'IS_VERCEL', False) else os.path.join(BASE_DIR, 'truck_maintenance_system.db')
                app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{sqlite_path}"
                db.engine.dispose()
                db.create_all()
                migrate_memo_columns(app)
                migrate_vehicle_columns(app)
                seed_initial_data(app)
                print(f"[Database Fallback] Offline SQLite database initialized and ready at {sqlite_path}.")
            except Exception as fallback_err:
                print(f"[Database Error] SQLite fallback failed: {fallback_err}")
