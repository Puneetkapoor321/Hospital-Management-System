from django.db import transaction
from django.shortcuts import get_object_or_404, render
from django.utils import timezone

from accounts.decorators import patient_required
from accounts.models import User
from doctors.models import AvailabilitySlot
from .models import Booking
from integrations.google_calendar import create_booking_events
from integrations.email_client import send_booking_confirmation_email


@patient_required
def doctor_list(request):
    doctors = User.objects.filter(role=User.ROLE_DOCTOR)
    return render(request, "bookings/doctor_list.html", {"doctors": doctors})


@patient_required
def doctor_slots(request, doctor_id):
    doctor = get_object_or_404(User, pk=doctor_id, role=User.ROLE_DOCTOR)
    slots = (
        AvailabilitySlot.objects.filter(
            doctor=doctor,
            is_booked=False,
            date__gte=timezone.localdate(),
        )
        .order_by("date", "start_time")
    )
    return render(request, "bookings/doctor_slots.html", {"doctor": doctor, "slots": slots})


@patient_required
def book_slot(request, slot_id):
    slot = get_object_or_404(AvailabilitySlot, pk=slot_id)

    if request.method == "POST":
        # Critical section: prevent race conditions using select_for_update
        with transaction.atomic():
            locked_slot = AvailabilitySlot.objects.select_for_update().get(pk=slot.pk)
            if locked_slot.is_booked or not locked_slot.is_future():
                return render(
                    request,
                    "bookings/booking_error.html",
                    {"message": "Slot is no longer available."},
                )

            booking = Booking.objects.create(
                doctor=locked_slot.doctor,
                patient=request.user,
                slot=locked_slot,
            )
            locked_slot.is_booked = True
            locked_slot.save()

        # Outside transaction: external integrations
        doctor_event_id, patient_event_id = create_booking_events(booking)
        if doctor_event_id or patient_event_id:
            booking.doctor_event_id = doctor_event_id or ""
            booking.patient_event_id = patient_event_id or ""
            booking.save(update_fields=["doctor_event_id", "patient_event_id"])

        send_booking_confirmation_email(booking)

        return render(request, "bookings/booking_success.html", {"booking": booking})

    return render(request, "bookings/booking_confirm.html", {"slot": slot})
