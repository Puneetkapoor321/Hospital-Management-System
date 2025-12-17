from django.urls import path

from . import views

app_name = "accounts"

urlpatterns = [
    path("", views.landing_page, name="landing"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("signup/doctor/", views.doctor_signup, name="doctor_signup"),
    path("signup/patient/", views.patient_signup, name="patient_signup"),
    path("dashboard/", views.dashboard, name="dashboard"),
]
