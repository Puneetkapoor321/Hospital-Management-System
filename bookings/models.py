from django.db import models
from django.utils import timezone

from accounts.models import User
from doctors.models import AvailabilitySlot


class Booking(models.Model):
    doctor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="doctor_bookings",
        limit_choices_to={"role": User.ROLE_DOCTOR},
    )
    patient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="patient_bookings",
        limit_choices_to={"role": User.ROLE_PATIENT},
    )
    slot = models.OneToOneField(
        AvailabilitySlot, on_delete=models.CASCADE, related_name="booking")
    created_at = models.DateTimeField(default=timezone.now)
    doctor_event_id = models.CharField(max_length=255, blank=True)
    patient_event_id = models.CharField(max_length=255, blank=True)

    def __str__(self) -> str:
        return f"{self.patient} -> {self.doctor} on {self.slot}"
