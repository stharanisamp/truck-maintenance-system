import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent

# Load environment variables from .env file, with fallback to .env.example
load_dotenv(os.path.join(BASE_DIR, ".env"), override=True)
if os.path.exists(os.path.join(BASE_DIR, ".env.example")):
    load_dotenv(os.path.join(BASE_DIR, ".env.example"), override=False)

def _has_placeholder(value, placeholders):
    if not value:
        return False
    val_lower = str(value).lower()
    for p in placeholders:
        if p in val_lower:
            return True
    return False

class Config:
    BASE_DIR = BASE_DIR
    SECRET_KEY = os.getenv("SECRET_KEY", "truck-secret-key-prod-antigravity-2026")
    
    # Environment detection
    IS_VERCEL = bool(os.getenv("VERCEL"))

    # Upload directories (use writable /tmp/uploads on Vercel serverless)
    if IS_VERCEL:
        UPLOAD_FOLDER = os.path.join("/tmp", "uploads")
    else:
        UPLOAD_FOLDER = os.path.join(BASE_DIR, "static", "uploads")
    MEMO_UPLOAD_FOLDER = os.path.join(UPLOAD_FOLDER, "memos")
    FUEL_UPLOAD_FOLDER = os.path.join(UPLOAD_FOLDER, "fuel_bills")
    PROFILE_UPLOAD_FOLDER = os.path.join(UPLOAD_FOLDER, "profiles")
    MAX_CONTENT_LENGTH = 32 * 1024 * 1024  # 32MB max
    
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "pdf", "webp"}
    
    # Supabase / Cloud API Configuration
    URL = os.getenv("URL", "")
    ANON_KEY = os.getenv("ANON_KEY", "")
    SUPABASE_URL = os.getenv("SUPABASE_URL", URL)
    SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY", ANON_KEY)
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
    GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")

    # Database configuration
    DB_MODE = os.getenv("DB_MODE", "offline").strip().lower()
    DB_TYPE = os.getenv("DB_TYPE", "sqlite").strip().lower()
    DB_USER = os.getenv("DB_USER", "root")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "")
    DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
    DB_PORT = os.getenv("DB_PORT", "3306")
    DB_NAME = os.getenv("DB_NAME", "truck_maintenance_system")

    # Resolve Database URL (supports DATABASE_URL, POSTGRES_URL, or SUPABASE_DATABASE_URL)
    raw_db_url = (
        os.getenv("DATABASE_URL")
        or os.getenv("POSTGRES_URL")
        or os.getenv("SUPABASE_DATABASE_URL")
        or ""
    ).strip()
    
    # Detect sample/dummy placeholders
    sample_indicators = ["your-project", "your_password", "sample", "placeholder", "example.com", "<", ">"]
    is_sample_db = _has_placeholder(raw_db_url, sample_indicators)

    # SQLite database file path (use /tmp on Vercel since root directory is read-only)
    sqlite_db_path = "/tmp/truck_maintenance_system.db" if IS_VERCEL else os.path.join(BASE_DIR, "truck_maintenance_system.db")

    # Force local offline SQLite if DB_MODE is offline
    if DB_MODE == "offline":
        IS_OFFLINE = True
        DATABASE_URL = f"sqlite:///{sqlite_db_path}"
    elif DB_TYPE == "mysql" and not IS_VERCEL:
        import urllib.parse
        pwd_part = f":{urllib.parse.quote_plus(DB_PASSWORD)}" if DB_PASSWORD else ""
        mysql_url = f"mysql+pymysql://{DB_USER}{pwd_part}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8mb4"
        
        # Test if MySQL server is reachable with configured credentials
        can_connect_mysql = False
        try:
            import pymysql
            _test_conn = pymysql.connect(
                host=DB_HOST,
                port=int(DB_PORT),
                user=DB_USER,
                password=DB_PASSWORD,
                connect_timeout=2
            )
            _test_conn.close()
            can_connect_mysql = True
        except Exception as _e:
            can_connect_mysql = False

        if can_connect_mysql:
            IS_OFFLINE = False
            DATABASE_URL = mysql_url
        else:
            IS_OFFLINE = True
            DATABASE_URL = f"sqlite:///{sqlite_db_path}"
    elif raw_db_url and not is_sample_db:
        IS_OFFLINE = False
        # Normalize postgresql prefix for SQLAlchemy
        if raw_db_url.startswith("postgres://"):
            raw_db_url = raw_db_url.replace("postgres://", "postgresql://", 1)
        DATABASE_URL = raw_db_url
    else:
        IS_OFFLINE = True
        DATABASE_URL = f"sqlite:///{sqlite_db_path}"

    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_recycle": 280,
        "pool_pre_ping": True
    }
    
    # Email / SMTP Settings (Supports MAIL_ID, MAIL_USERNAME, PASS, APP_PASS, MAIL_PASSWORD)
    MAIL_SERVER = os.getenv("MAIL_SERVER", "smtp.gmail.com")
    MAIL_PORT = int(os.getenv("MAIL_PORT", 587))
    MAIL_USE_TLS = os.getenv("MAIL_USE_TLS", "True").lower() in ("true", "1")
    
    raw_mail = (os.getenv("MAIL_ID") or os.getenv("MAIL_USERNAME") or "").strip()
    raw_pass = (os.getenv("PASS") or os.getenv("APP_PASS") or os.getenv("MAIL_PASSWORD") or "").replace(" ", "").strip()

    is_sample_mail = _has_placeholder(raw_mail, ["your-email", "sample", "example.com", "yourgmail@gmail.com"])
    is_sample_pass = _has_placeholder(raw_pass, ["your-", "sample", "placeholder", "app-password"])

    MAIL_USERNAME = "" if is_sample_mail else raw_mail
    MAIL_PASSWORD = "" if is_sample_pass else raw_pass
    MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER") or (MAIL_USERNAME if MAIL_USERNAME else "noreply@truckmaintenancesystem.com")
    DEV_MODE_OTP = False
    ENABLE_DRIVER_OTP = False
