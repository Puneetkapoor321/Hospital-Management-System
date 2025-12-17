from datetime import datetime

from django.utils import timezone
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

from .models import GoogleCredentials

SCOPES = ["https://www.googleapis.com/auth/calendar"]


def _get_credentials(user):
    try:
        gc = user.google_credentials
    except GoogleCredentials.DoesNotExist:
        return None
    # credentials_json is stored as a JSON string
    return Credentials.from_authorized_user_info(eval(gc.credentials_json), SCOPES)


def _build_service(creds):
    return build("calendar", "v3", credentials=creds)


def create_booking_events(booking):
    """
    Create events for both doctor and patient (if they have connected Google Calendar).
    Returns (doctor_event_id, patient_event_id).
    For demo, this will be a no-op if credentials are not configured.
    """
    doctor_creds = _get_credentials(booking.doctor)
    patient_creds = _get_credentials(booking.patient)

    if not doctor_creds and not patient_creds:
        return None, None

    slot = booking.slot
    start = timezone.make_aware(datetime.combine(slot.date, slot.start_time))
    end = timezone.make_aware(datetime.combine(slot.date, slot.end_time))

    doctor_event_id = None
    patient_event_id = None

    if doctor_creds:
        service = _build_service(doctor_creds)
        body = {
            "summary": f"Appointment with {booking.patient.get_full_name() or booking.patient.username}",
            "description": "Hospital appointment",
            "start": {"dateTime": start.isoformat()},
            "end": {"dateTime": end.isoformat()},
        }
        event = service.events().insert(calendarId="primary", body=body).execute()
        doctor_event_id = event.get("id")

    if patient_creds:
        service = _build_service(patient_creds)
        body = {
            "summary": f"Appointment with Dr. {booking.doctor.get_full_name() or booking.doctor.username}",
            "description": "Hospital appointment",
            "start": {"dateTime": start.isoformat()},
            "end": {"dateTime": end.isoformat()},
        }
        event = service.events().insert(calendarId="primary", body=body).execute()
        patient_event_id = event.get("id")

    return doctor_event_id, patient_event_id
