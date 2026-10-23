import random
from datetime import datetime, timedelta, timezone
from flask import current_app, session
from flask_mail import Mail, Message
from models import db, OtpCode

mail = Mail()

def generate_and_send_otp(email, purpose="LOGIN"):
    """
    Generates a 6-digit OTP, stores it in otp_codes table,
    attempts email dispatch via Gmail SMTP, and returns (otp, sent).
    """
    # Generate 6-digit random code
    otp = f"{random.randint(100000, 999999)}"
    expires_at = datetime.now(timezone.utc) + timedelta(minutes=10)

    # Invalidate previous OTPs for this email/purpose
    OtpCode.query.filter_by(email=email, purpose=purpose, is_used=False).update({"is_used": True})
    
    otp_record = OtpCode(
        email=email,
        otp_code=otp,
        purpose=purpose,
        expires_at=expires_at,
        is_used=False
    )
    db.session.add(otp_record)
    db.session.commit()

    # Determine subject and title based on purpose
    if purpose == "REGISTRATION":
        subject = f"{otp} is your Truck Maintenance System Registration OTP"
        headline = "Account Registration Verification"
        greeting = "Hello,"
        detail = "Use the 6-digit verification code below to complete your account registration:"
    elif purpose == "PASSWORD_RESET":
        subject = f"{otp} is your Truck Maintenance System Password Reset OTP"
        headline = "Password Reset Request"
        greeting = "Hello,"
        detail = "Use the 6-digit code below to securely reset your account password:"
    elif purpose == "ADMIN_LOGIN":
        subject = f"{otp} is your Admin Login Security OTP"
        headline = "Admin & Fleet Owner Two-Factor Authentication"
        greeting = "Hello Admin,"
        detail = "A sign-in attempt was initiated for your Administrator account. Enter this 6-digit verification code to proceed:"
    elif purpose in ("DRIVER_LOGIN", "LOGIN"):
        subject = f"{otp} is your Driver Login Security OTP"
        headline = "Driver Portal Two-Factor Authentication"
        greeting = "Hello Driver,"
        detail = "A sign-in attempt was initiated for your Driver account. Enter this 6-digit verification code to proceed:"
    else:
        subject = f"{otp} is your Truck Maintenance System OTP"
        headline = f"Security Verification ({purpose})"
        greeting = "Hello,"
        detail = f"Your One-Time Password (OTP) for {purpose} is:"

    plain_body = f"{greeting}\n\n{detail}\n\nOTP Code: {otp}\n\nThis OTP is valid for 10 minutes.\nDo not share this code with anyone.\n\nTruck Maintenance System Security Team"

    html_body = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
</head>
<body style="margin: 0; padding: 20px; background-color: #f8fafc; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;">
    <div style="max-width: 520px; margin: 0 auto; background: #ffffff; border-radius: 12px; overflow: hidden; border: 1px solid #e2e8f0; box-shadow: 0 4px 12px rgba(0,0,0,0.05);">
        <div style="background: linear-gradient(135deg, #1e293b, #0f172a); padding: 26px 24px; text-align: center;">
            <h2 style="color: #ffffff; margin: 0; font-size: 20px; font-weight: 700; letter-spacing: -0.5px;">TRUCK MAINTENANCE SYSTEM</h2>
            <p style="color: #94a3b8; margin: 6px 0 0; font-size: 13px;">{headline}</p>
        </div>
        <div style="padding: 32px 28px; text-align: center;">
            <p style="color: #334155; font-size: 15px; margin: 0 0 12px; text-align: left;">{greeting}</p>
            <p style="color: #475569; font-size: 14px; margin: 0 0 24px; text-align: left; line-height: 1.5;">{detail}</p>
            <div style="display: inline-block; background: #eff6ff; border: 2px dashed #3b82f6; border-radius: 10px; padding: 14px 36px; margin: 8px 0 24px;">
                <span style="font-family: 'Courier New', Courier, monospace; font-size: 34px; font-weight: 800; letter-spacing: 8px; color: #1d4ed8;">{otp}</span>
            </div>
            <p style="color: #64748b; font-size: 13px; margin: 0; line-height: 1.5;">
                ⏱ This code is valid for <strong>10 minutes</strong>.<br>
                🔒 For your security, never share this code with anyone.
            </p>
        </div>
        <div style="background: #f1f5f9; padding: 14px 20px; text-align: center; border-top: 1px solid #e2e8f0;">
            <p style="color: #94a3b8; font-size: 11px; margin: 0;">Automated Security Message &bull; Truck Maintenance System &copy; 2026</p>
        </div>
    </div>
</body>
</html>"""

    # Try sending via Flask-Mail
    sent = False
    try:
        username = current_app.config.get("MAIL_USERNAME")
        password = current_app.config.get("MAIL_PASSWORD")
        sender = current_app.config.get("MAIL_DEFAULT_SENDER") or username
        if username and password:
            msg = Message(
                subject=subject,
                sender=f"Truck Maintenance System <{username}>",
                recipients=[email],
                body=plain_body,
                html=html_body
            )
            mail.send(msg)
            sent = True
            print(f"[Email Service] Successfully sent real OTP email to {email}")
        else:
            print(f"[Email Service] Notice: MAIL_USERNAME or MAIL_PASSWORD not configured in .env.")
    except Exception as e:
        print(f"[Email Service Error] Failed to send email to {email}: {e}")

    return otp, sent

def verify_otp(email, entered_code, purpose="LOGIN"):
    """
    Verifies that the entered OTP is valid, unused, and not expired.
    """
    entered_code = str(entered_code).strip()
    record = OtpCode.query.filter_by(
        email=email,
        otp_code=entered_code,
        purpose=purpose,
        is_used=False
    ).order_by(OtpCode.id.desc()).first()

    # If purpose specific match not found, check any active unused OTP for this email
    if not record:
        record = OtpCode.query.filter_by(
            email=email,
            otp_code=entered_code,
            is_used=False
        ).order_by(OtpCode.id.desc()).first()

    if not record:
        return False, "Invalid OTP code. Please check and try again."

    # Compare UTC timestamps
    now_utc = datetime.now(timezone.utc)
    exp = record.expires_at
    if exp.tzinfo is None:
        exp = exp.replace(tzinfo=timezone.utc)

    if now_utc > exp:
        return False, "This OTP has expired. Please request a new code."

    # Mark as used
    record.is_used = True
    db.session.commit()
    return True, "OTP verified successfully."
