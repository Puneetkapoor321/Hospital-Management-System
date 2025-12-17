from django.urls import path

from . import views

app_name = "doctors"

urlpatterns = [
    path("availability/", views.availability_list, name="availability_list"),
    path("availability/create/", views.availability_create,
         name="availability_create"),
    path("availability/<int:pk>/edit/",
         views.availability_update, name="availability_update"),
    path("availability/<int:pk>/delete/",
         views.availability_delete, name="availability_delete"),
]
