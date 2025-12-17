from django.urls import path

from . import views

app_name = "bookings"

urlpatterns = [
    path("doctors/", views.doctor_list, name="doctor_list"),
    path("doctors/<int:doctor_id>/slots/",
         views.doctor_slots, name="doctor_slots"),
    path("slots/<int:slot_id>/book/", views.book_slot, name="book_slot"),
]
