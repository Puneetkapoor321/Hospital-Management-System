from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("doctors/", include("doctors.urls")),
    path("bookings/", include("bookings.urls")),
    # integrations (e.g. Google OAuth) URLs could be added here
    path("", views.root_view, name="root"),  # Root URL handles both HTML and JSON
]
