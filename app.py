import os
import subprocess

from flask import Flask, redirect, render_template, session, url_for

from config import Config
from database import init_db
from email_service import mail
from models import Notification, db
from routes.admin_routes import admin_bp
from routes.api_routes import api_bp
from routes.auth_routes import auth_bp
from routes.driver_routes import driver_bp


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    mail.init_app(app)

    # Register Blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(driver_bp)
    app.register_blueprint(api_bp)

    # Context processor for notifications and user details
    @app.context_processor
    def inject_global_vars():
        from datetime import datetime, timezone
        unread_count = 0
        latest_notifications = []
        if session.get('role') == 'admin':
            unread_count = Notification.query.filter_by(is_read=False).count()
            latest_notifications = Notification.query.order_by(Notification.id.desc()).limit(5).all()
        return {
            'today': datetime.now(timezone.utc).date(),
            'unread_notifications_count': unread_count,
            'header_notifications': latest_notifications,
            'current_user_name': session.get('user_name', 'Guest'),
            'current_role': session.get('role', None)
        }

    # Template filters
    @app.template_filter('currency')
    def currency_filter(val):
        try:
            return f"₹{float(val):,.2f}"
        except (ValueError, TypeError):
            return f"₹{val}"

    @app.template_filter('date_fmt')
    def date_filter(d):
        if not d:
            return "—"
        if hasattr(d, 'strftime'):
            return d.strftime('%d %b %Y')
        return str(d)

    # Root route and Vercel serverless entry route
    @app.route('/')
    @app.route('/api/index')
    def index():
        role = session.get('role')
        if role == 'admin':
            return redirect(url_for('admin.dashboard'))
        elif role == 'driver':
            return redirect(url_for('driver.dashboard'))
        return redirect(url_for('auth.login'))

    # Custom 404 handler
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    # Vercel upload file server: serves dynamic uploads saved in writable /tmp/uploads
    if getattr(Config, 'IS_VERCEL', False):
        from flask import send_from_directory
        @app.route('/static/uploads/<path:filename>')
        def serve_vercel_uploads(filename):
            tmp_path = os.path.join(Config.UPLOAD_FOLDER, filename)
            if os.path.exists(tmp_path):
                return send_from_directory(Config.UPLOAD_FOLDER, filename)
            static_uploads = os.path.join(Config.BASE_DIR, "static", "uploads")
            return send_from_directory(static_uploads, filename)

    # Initialize Database and seed data
    init_db(app)

    return app

app = create_app()

if __name__ == '__main__':
    # Run development server
    port = int(os.environ.get('PORT', '5000'))

    # Auto-release port 5000 if occupied by any stale background process so VS Code runs cleanly
    try:
        net_lines = subprocess.check_output('netstat -ano', shell=True).decode('utf-8', errors='ignore').splitlines()
        my_pid = os.getpid()
        for line in net_lines:
            if f':{port} ' in line and 'LISTENING' in line:
                parts = line.strip().split()
                stale_pid = int(parts[-1])
                if stale_pid != my_pid:
                    subprocess.run(f'taskkill /F /PID {stale_pid}', shell=True, capture_output=True, check=False)
    except (subprocess.SubprocessError, OSError, ValueError):
        pass

    mode_text = "OFFLINE (Local SQLite)" if Config.IS_OFFLINE else "ONLINE"
    print("\n=======================================================")
    print("  TRUCK MAINTENANCE SYSTEM - AI MEMO & FLEET FINANCE")
    print(f"  Mode: {mode_text}")
    print(f"  Server URL: http://127.0.0.1:{port}")
    print("  Admin Login: stharanisamp@gmail.com / admin123")
    print("  Driver Login: murugan@truck.com / driver123")
    # Server active with multi-threaded request processing to prevent socket timeouts
    app.run(host='0.0.0.0', port=port, debug=False, threaded=True)
