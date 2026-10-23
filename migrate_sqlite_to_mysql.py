import os
import sys
import sqlite3
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

def migrate():
    print("=" * 65)
    print("   MIGRATE DATA FROM SQLITE TO MYSQL (TRUCK MAINTENANCE SYSTEM)")
    print("=" * 65)

    sqlite_path = os.path.join(os.path.dirname(__file__), "truck_maintenance_system.db")
    if not os.path.exists(sqlite_path):
        print(f"[-] SQLite database file not found at {sqlite_path}. Nothing to migrate.")
        return

    from app import create_app
    from models import db, Admin, Driver, Vehicle, Customer, Memo, MemoExpense, FuelBill, OtpCode, Notification, ActivityLog

    s_conn = sqlite3.connect(sqlite_path)
    s_conn.row_factory = sqlite3.Row
    s_cur = s_conn.cursor()

    app = create_app()
    with app.app_context():
        # Ensure MySQL tables exist
        db.create_all()

        tables_to_migrate = [
            (Admin, "admins"),
            (Vehicle, "vehicles"),
            (Driver, "drivers"),
            (Customer, "customers"),
            (Memo, "memos"),
            (MemoExpense, "memo_expenses"),
            (FuelBill, "fuel_bills"),
            (Notification, "notifications"),
            (ActivityLog, "activity_logs")
        ]

        print("[*] Reading data from SQLite and importing into MySQL...")

        for model, table_name in tables_to_migrate:
            try:
                rows = s_cur.execute(f"SELECT * FROM {table_name}").fetchall()
                if not rows:
                    continue
                cols = [desc[0] for desc in s_cur.description]
                model_cols = [c.name for c in model.__table__.columns]
                valid_cols = [c for c in cols if c in model_cols]

                count = 0
                for r in rows:
                    row_dict = {col: r[col] for col in valid_cols if r[col] is not None}
                    # Check if already in MySQL
                    if 'id' in row_dict and model.query.get(row_dict['id']):
                        continue
                    obj = model(**row_dict)
                    db.session.add(obj)
                    count += 1
                db.session.commit()
                print(f"  [OK] {table_name:18}: {count} records imported")
            except Exception as e:
                db.session.rollback()
                print(f"  [ERR] {table_name:18}: note - {e}")

    s_conn.close()
    print("\n[SUCCESS] Data migration completed cleanly!")

if __name__ == "__main__":
    migrate()
