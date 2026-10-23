import os
import sys
import socket
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

def check_port(host, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)
    try:
        s.connect((host, port))
        s.close()
        return True
    except Exception:
        return False

def check_mysql_services():
    import subprocess
    try:
        res = subprocess.run(["powershell", "-NoProfile", "-Command", "Get-Service *mysql* | Select-Object -Property Name, Status, DisplayName | Format-Table -HideTableHeaders"], capture_output=True, text=True)
        return res.stdout.strip()
    except Exception:
        return ""

def main():
    print("=" * 60)
    print("      XAMPP / MYSQL DATABASE CONNECTION CHECKER")
    print("=" * 60)

    host = os.getenv("DB_HOST", "127.0.0.1")
    port = int(os.getenv("DB_PORT", 3306))
    user = os.getenv("DB_USER", "root")
    password = os.getenv("DB_PASSWORD", "")
    db_name = os.getenv("DB_NAME", "truck_maintenance_system")

    print(f"[*] Target Host: {host}")
    print(f"[*] Target Port: {port}")
    print(f"[*] User:        {user}")
    print(f"[*] Password:    {'[EMPTY - Default XAMPP]' if not password else '********'}")
    print(f"[*] Database:    {db_name}")
    print("-" * 60)

    # 1. Check Port
    print(f"1. Checking if port {port} is open...")
    if not check_port(host, port):
        print(f"   [FAILED] Port {port} is NOT responding!")
        print("   -> Tip: Please open XAMPP Control Panel and click 'Start' next to MySQL.")
        sys.exit(1)
    print(f"   [OK] Port {port} is listening!")

    # 2. Check PyMySQL Connection
    print(f"\n2. Connecting to MySQL Server...")
    import pymysql
    try:
        conn = pymysql.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            charset='utf8mb4',
            connect_timeout=5
        )
        print("   [OK] Successfully connected to MySQL Server!")
    except pymysql.err.OperationalError as e:
        err_code, err_msg = e.args[0], e.args[1] if len(e.args) > 1 else str(e)
        print(f"   [FAILED] Could not connect: {err_msg} (Error Code: {err_code})")
        
        if err_code == 1045: # Access denied
            print("\n   [DIAGNOSIS]: Access denied for user 'root'.")
            svc_info = check_mysql_services()
            if "MySQL80" in svc_info and "Running" in svc_info:
                print("   [!] IMPORTANT CONFLICT DETECTED:")
                print("   Windows Service 'MySQL80' (standalone MySQL Server) is currently RUNNING on port 3306!")
                print("   If you want to use XAMPP MySQL:")
                print("     1. Open PowerShell as Admin and run: Stop-Service MySQL80")
                print("     2. Then open XAMPP Control Panel and click 'Start' on MySQL.")
                print("   If you want to use this MySQL80 instead:")
                print("     Update DB_PASSWORD in your .env file with your MySQL80 root password.")
            else:
                print("   -> Your MySQL root user has a password. Please enter it in the .env file:")
                print("      DB_PASSWORD=your_password_here")
        sys.exit(1)
    except Exception as e:
        print(f"   [FAILED] Connection error: {e}")
        sys.exit(1)

    # 3. Check / Create Database
    print(f"\n3. Checking database '{db_name}'...")
    try:
        with conn.cursor() as cur:
            cur.execute(f"CREATE DATABASE IF NOT EXISTS `{db_name}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
            print(f"   [OK] Database '{db_name}' is verified / created!")
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"   [FAILED] Error creating database: {e}")
        sys.exit(1)

    # 4. Initialize Tables via SQLAlchemy
    print(f"\n4. Initializing tables in MySQL using SQLAlchemy models...")
    try:
        from app import create_app
        from models import db, Admin, Driver, Vehicle, Customer, Memo, FuelBill
        app = create_app()
        with app.app_context():
            db.create_all()
            print("   [OK] All tables successfully created in MySQL!")
            
            # Auto-migrate data from SQLite if MySQL is newly created
            if Admin.query.count() == 0:
                print("   [*] Migrating records from truck_maintenance_system.db to MySQL...")
                try:
                    from migrate_sqlite_to_mysql import migrate
                    migrate()
                except Exception as mig_err:
                    print(f"   [-] Auto-migration note: {mig_err}")
            
            # Count records
            admins = Admin.query.count()
            drivers = Driver.query.count()
            vehicles = Vehicle.query.count()
            customers = Customer.query.count()
            memos = Memo.query.count()
            fuels = FuelBill.query.count()
            print("\n" + "=" * 60)
            print(f"   DATABASE STATUS: READY & CONNECTED TO MYSQL")
            print("=" * 60)
            print(f"   - Admins:    {admins}")
            print(f"   - Drivers:   {drivers}")
            print(f"   - Vehicles:  {vehicles}")
            print(f"   - Customers: {customers}")
            print(f"   - Memos:     {memos}")
            print(f"   - FuelBills: {fuels}")
            print("=" * 60)
            print("\nTo start your project with MySQL, run:")
            print("   python app.py\n")
    except Exception as e:
        print(f"   [FAILED] Error initializing tables: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
