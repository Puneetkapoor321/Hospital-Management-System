from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .decorators import doctor_required, patient_required
from .forms import DoctorSignUpForm, LoginForm, PatientSignUpForm
from .models import User
from integrations.email_client import send_signup_welcome_email


def landing_page(request):
    """Landing page for unauthenticated users"""
    if request.user.is_authenticated:
        return redirect("accounts:dashboard")
    return render(request, "landing.html")


def doctor_signup(request):
    if request.method == "POST":
        form = DoctorSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            send_signup_welcome_email(user)
            return redirect("accounts:dashboard")
    else:
        form = DoctorSignUpForm()
    return render(request, "accounts/doctor_signup.html", {"form": form})


def patient_signup(request):
    if request.method == "POST":
        form = PatientSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            send_signup_welcome_email(user)
            return redirect("accounts:dashboard")
    else:
        form = PatientSignUpForm()
    return render(request, "accounts/patient_signup.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("accounts:dashboard")
    else:
        form = LoginForm(request)
    return render(request, "accounts/login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("accounts:landing")


@login_required
def dashboard(request):
    if isinstance(request.user, User):
        if request.user.is_doctor():
            from doctors.models import AvailabilitySlot
            from bookings.models import Booking
            slots = AvailabilitySlot.objects.filter(doctor=request.user).order_by('-date', 'start_time')
            bookings = Booking.objects.filter(doctor=request.user).order_by('slot__date', 'slot__start_time')
            return render(request, "accounts/doctor_dashboard.html", {
                'slots': slots,
                'bookings': bookings
            })
        if request.user.is_patient():
            from bookings.models import Booking
            from django.utils import timezone
            doctors = User.objects.filter(role=User.ROLE_DOCTOR)
            bookings = Booking.objects.filter(patient=request.user).order_by('slot__date', 'slot__start_time')
            return render(request, "accounts/patient_dashboard.html", {
                'doctors': doctors,
                'bookings': bookings
            })
    return redirect("accounts:login")


@doctor_required
def doctor_only_view(request):
    return render(request, "accounts/doctor_dashboard.html")


@patient_required
def patient_only_view(request):
    return render(request, "accounts/patient_dashboard.html")
