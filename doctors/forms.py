from datetime import datetime

from django import forms
from django.utils import timezone

from .models import AvailabilitySlot


class AvailabilitySlotForm(forms.ModelForm):
    class Meta:
        model = AvailabilitySlot
        fields = ["date", "start_time", "end_time"]

    def clean(self):
        cleaned = super().clean()
        date = cleaned.get("date")
        start = cleaned.get("start_time")
        end = cleaned.get("end_time")

        if start and end and start >= end:
            raise forms.ValidationError("End time must be after start time.")

        if date and start:
            dt = datetime.combine(date, start)
            aware_dt = timezone.make_aware(dt)
            if aware_dt <= timezone.now():
                raise forms.ValidationError(
                    "Availability must be in the future.")

        return cleaned
