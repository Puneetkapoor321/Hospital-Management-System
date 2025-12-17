import os

import requests

EMAIL_LAMBDA_URL = os.environ.get("EMAIL_LAMBDA_URL")


def _post_email(payload: dict) -> None:
    """Send JSON payload to the serverless email service."""
    if not EMAIL_LAMBDA_URL:
        return
    try:
        requests.post(EMAIL_LAMBDA_URL, json=payload, timeout=5)
    except Exception:
        # In demo mode we silently ignore email errors; in production log this.
        pass


def send_signup_welcome_email(user):
    payload = {
        "action": "SIGNUP_WELCOME",
        "to_email": user.email,
        "variables": {
            "name": user.get_full_name() or user.username,
            "role": getattr(user, "role", ""),
        },
    }
    _post_email(payload)


def send_booking_confirmation_email(booking):
    slot = booking.slot
    payload = {
        "action": "BOOKING_CONFIRMATION",
        "to_email": booking.patient.email,
        "variables": {
            "patient_name": booking.patient.get_full_name() or booking.patient.username,
            "doctor_name": booking.doctor.get_full_name() or booking.doctor.username,
            "date": str(slot.date),
            "start_time": str(slot.start_time),
            "end_time": str(slot.end_time),
        },
    }
    _post_email(payload)
