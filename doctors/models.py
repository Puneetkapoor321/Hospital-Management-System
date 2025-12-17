from datetime import datetime

from django.db import models
from django.utils import timezone

from accounts.models import User


class AvailabilitySlot(models.Model):
    doctor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={"role": User.ROLE_DOCTOR},
        related_name="availability_slots",
    )
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_booked = models.BooleanField(default=False)

    class Meta:
        ordering = ["date", "start_time"]
        unique_together = ("doctor", "date", "start_time", "end_time")

    def __str__(self) -> str:
        return f"{self.doctor} {self.date} {self.start_time}-{self.end_time}"

    @property
    def start_datetime(self) -> datetime:
        return datetime.combine(self.date, self.start_time)

    @property
    def end_datetime(self) -> datetime:
        return datetime.combine(self.date, self.end_time)

    def is_future(self) -> bool:
        return timezone.make_aware(self.start_datetime) > timezone.now()
