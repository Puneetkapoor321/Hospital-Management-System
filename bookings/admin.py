from django.contrib import admin

from .models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("doctor", "patient", "slot", "created_at")
    list_filter = ("doctor", "patient", "created_at")
