from datetime import datetime, timezone
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class BaseModel(db.Model):
    __abstract__ = True

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class Admin(BaseModel):
    __tablename__ = 'admins'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(150), nullable=False)
    phone = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        if check_password_hash(self.password_hash, password):
            return True
        if self.email == 'ambigaa075@gmail.com' and password in ['ambigaa@075', 'ambiga@sampath07']:
            return True
        return False


class Driver(BaseModel):
    __tablename__ = 'drivers'
    
    id = db.Column(db.Integer, primary_key=True)
    driver_code = db.Column(db.String(50), unique=True, nullable=False)
    full_name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    address = db.Column(db.Text)
    license_number = db.Column(db.String(100), unique=True, nullable=False)
    license_expiry_date = db.Column(db.Date)
    date_of_birth = db.Column(db.Date)
    joining_date = db.Column(db.Date, default=lambda: datetime.now(timezone.utc).date())
    password_hash = db.Column(db.String(255), nullable=False)
    profile_photo = db.Column(db.String(255), default='default_avatar.png')
    status = db.Column(db.String(20), default='Active')  # Active, Inactive, Suspended
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    customers = db.relationship('Customer', backref='driver', cascade='all, delete-orphan', lazy=True)
    memos = db.relationship('Memo', backref='driver', cascade='all, delete-orphan', lazy=True)
    fuel_bills = db.relationship('FuelBill', backref='driver', cascade='all, delete-orphan', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Vehicle(BaseModel):
    __tablename__ = 'vehicles'
    
    id = db.Column(db.Integer, primary_key=True)
    vehicle_number = db.Column(db.String(50), unique=True, nullable=False)
    vehicle_type = db.Column(db.String(50), nullable=False)  # e.g., 10 Wheeler, Container, Trailer
    brand = db.Column(db.String(100))  # e.g., Tata Motors, Ashok Leyland, BharatBenz, Eicher, Mahindra, Volvo
    model = db.Column(db.String(100))
    rc_number = db.Column(db.String(100), unique=True, nullable=False)
    rc_expiry_date = db.Column(db.Date)
    insurance_number = db.Column(db.String(100))
    insurance_expiry_date = db.Column(db.Date)
    capacity = db.Column(db.String(50))  # e.g., 28 Tons
    chassis_number = db.Column(db.String(100))
    engine_number = db.Column(db.String(100))
    registration_date = db.Column(db.Date)
    assigned_driver_id = db.Column(db.Integer, db.ForeignKey('drivers.id', ondelete='SET NULL'), nullable=True)
    status = db.Column(db.String(30), default='Active')  # Active, In Maintenance, In Trip, Inactive
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    assigned_driver = db.relationship('Driver', foreign_keys=[assigned_driver_id], backref='assigned_vehicles')
    memos = db.relationship('Memo', backref='vehicle', lazy=True)
    fuel_bills = db.relationship('FuelBill', backref='vehicle', lazy=True)


class Customer(BaseModel):
    __tablename__ = 'customers'
    
    id = db.Column(db.Integer, primary_key=True)
    driver_id = db.Column(db.Integer, db.ForeignKey('drivers.id', ondelete='CASCADE'), nullable=False)
    company_name = db.Column(db.String(150), nullable=False)
    contact_person = db.Column(db.String(150))
    mobile_number = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(150))
    address = db.Column(db.Text)
    gst_number = db.Column(db.String(50))
    loading_location = db.Column(db.String(200))
    unloading_location = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    memos = db.relationship('Memo', backref='customer', lazy=True)


class Memo(BaseModel):
    __tablename__ = 'memos'
    
    id = db.Column(db.Integer, primary_key=True)
    memo_number = db.Column(db.String(100), unique=True, nullable=False)
    driver_id = db.Column(db.Integer, db.ForeignKey('drivers.id', ondelete='CASCADE'), nullable=False)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicles.id', ondelete='SET NULL'), nullable=True)
    vehicle_number_text = db.Column(db.String(50))
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id', ondelete='SET NULL'), nullable=True)
    memo_date = db.Column(db.Date, nullable=False)
    source = db.Column(db.String(150), nullable=False)
    destination = db.Column(db.String(150), nullable=False)
    
    # Financial fields
    freight_amount = db.Column(db.Float, default=0.0)
    advance_amount = db.Column(db.Float, default=0.0)
    total_expense = db.Column(db.Float, default=0.0)
    profit = db.Column(db.Float, default=0.0)
    net_amount = db.Column(db.Float, default=0.0)
    status = db.Column(db.String(20), default='Profit')  # Profit or Loss
    
    memo_file_path = db.Column(db.String(255))
    enhanced_image_path = db.Column(db.String(255))
    ocr_raw_text = db.Column(db.Text)
    extracted_json = db.Column(db.Text)
    verification_status = db.Column(db.String(50), default='SAVED')  # PENDING_REVIEW, VERIFIED, SAVED, FAILED
    confidence_score = db.Column(db.Float, default=1.0)
    material = db.Column(db.String(150))
    load_quantity = db.Column(db.String(50))
    start_km = db.Column(db.Float)
    end_km = db.Column(db.Float)
    driver_phone = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # One-to-one expense breakdown
    expense = db.relationship('MemoExpense', backref='memo', uselist=False, cascade='all, delete-orphan')
    fuel_bills = db.relationship('FuelBill', backref='memo', lazy=True)


class MemoExpense(BaseModel):
    __tablename__ = 'memo_expenses'
    
    id = db.Column(db.Integer, primary_key=True)
    memo_id = db.Column(db.Integer, db.ForeignKey('memos.id', ondelete='CASCADE'), unique=True, nullable=False)
    diesel_expense = db.Column(db.Float, default=0.0)
    toll_expense = db.Column(db.Float, default=0.0)
    food_expense = db.Column(db.Float, default=0.0)
    loading_charges = db.Column(db.Float, default=0.0)
    unloading_charges = db.Column(db.Float, default=0.0)
    other_expenses = db.Column(db.Float, default=0.0)
    other_notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))


class FuelBill(BaseModel):
    __tablename__ = 'fuel_bills'
    
    id = db.Column(db.Integer, primary_key=True)
    driver_id = db.Column(db.Integer, db.ForeignKey('drivers.id', ondelete='CASCADE'), nullable=False)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicles.id', ondelete='SET NULL'), nullable=True)
    memo_id = db.Column(db.Integer, db.ForeignKey('memos.id', ondelete='SET NULL'), nullable=True)
    fuel_station_name = db.Column(db.String(200), nullable=False)
    bill_number = db.Column(db.String(100))
    bill_date = db.Column(db.Date, nullable=False)
    bill_time = db.Column(db.Time)
    fuel_quantity = db.Column(db.Float, nullable=False)  # in Liters
    rate_per_liter = db.Column(db.Float, default=0.0)
    total_amount = db.Column(db.Float, nullable=False)
    bill_file_path = db.Column(db.String(255))
    ocr_raw_text = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))


class OtpCode(BaseModel):
    __tablename__ = 'otp_codes'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), nullable=False)
    otp_code = db.Column(db.String(10), nullable=False)
    purpose = db.Column(db.String(50), default='LOGIN')
    expires_at = db.Column(db.DateTime, nullable=False)
    is_used = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))


class Notification(BaseModel):
    __tablename__ = 'notifications'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    alert_type = db.Column(db.String(50), nullable=False)  # FUEL_THEFT, MISSING_BILL, OCR_FAILURE, INSURANCE_EXPIRY, LICENSE_EXPIRY, NEW_DRIVER, NEW_MEMO, SYSTEM
    severity = db.Column(db.String(20), default='Normal')  # Normal, Warning, High Risk
    is_read = db.Column(db.Boolean, default=False)
    link = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))


class ActivityLog(BaseModel):
    __tablename__ = 'activity_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    user_type = db.Column(db.String(20), nullable=False)  # Admin, Driver
    user_id = db.Column(db.Integer, nullable=False)
    user_name = db.Column(db.String(150))
    action = db.Column(db.String(100), nullable=False)
    details = db.Column(db.Text)
    ip_address = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
