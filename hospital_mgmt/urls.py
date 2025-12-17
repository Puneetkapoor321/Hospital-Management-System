from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("doctors/", include("doctors.urls")),
    path("bookings/", include("bookings.urls")),
    # integrations (e.g. Google OAuth) URLs could be added here
    path("", RedirectView.as_view(
        pattern_name="accounts:landing", permanent=False)),
]
