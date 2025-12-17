from django.contrib import admin

from .models import AvailabilitySlot


@admin.register(AvailabilitySlot)
class AvailabilitySlotAdmin(admin.ModelAdmin):
    list_display = ("doctor", "date", "start_time", "end_time", "is_booked")
    list_filter = ("doctor", "date", "is_booked")
