import json
import os
import smtplib
from email.mime.text import MIMEText

SMTP_HOST = os.environ.get("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.environ.get("SMTP_PORT", "587"))
SMTP_USER = os.environ.get("SMTP_USER")
SMTP_PASSWORD = os.environ.get("SMTP_PASSWORD")
FROM_EMAIL = os.environ.get("FROM_EMAIL", SMTP_USER)


def _send_email(to_email: str, subject: str, body: str) -> None:
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = FROM_EMAIL
    msg["To"] = to_email

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.starttls()
        if SMTP_USER and SMTP_PASSWORD:
            server.login(SMTP_USER, SMTP_PASSWORD)
        server.sendmail(FROM_EMAIL, [to_email], msg.as_string())


def _render_signup_welcome(vars_: dict):
    name = vars_.get("name", "User")
    role = vars_.get("role", "")
    subject = "Welcome to Hospital Management"
    body = f"Hello {name},\n\nWelcome to our Hospital Management system as a {role}.\n\nRegards,\nHospital"
    return subject, body


def _render_booking_confirmation(vars_: dict):
    subject = "Your Appointment is Confirmed"
    body = (
        f"Hello {vars_.get('patient_name', 'Patient')},\n\n"
        f"Your appointment with Dr. {vars_.get('doctor_name')} is confirmed on "
        f"{vars_.get('date')} from {vars_.get('start_time')} to {vars_.get('end_time')}.\n\n"
        "Regards,\nHospital"
    )
    return subject, body


def handle_email(event, context):
    try:
        body = json.loads(event.get("body") or "{}")
        action = body.get("action")
        to_email = body.get("to_email")
        variables = body.get("variables", {})

        if not to_email or not action:
            return {"statusCode": 400, "body": json.dumps({"error": "Missing fields"})}

        if action == "SIGNUP_WELCOME":
            subject, text = _render_signup_welcome(variables)
        elif action == "BOOKING_CONFIRMATION":
            subject, text = _render_booking_confirmation(variables)
        else:
            return {"statusCode": 400, "body": json.dumps({"error": "Unknown action"})}

        _send_email(to_email, subject, text)
        return {"statusCode": 200, "body": json.dumps({"status": "sent"})}
    except Exception as exc:  # pragma: no cover - for safety in Lambda
        return {"statusCode": 500, "body": json.dumps({"error": str(exc)})}
