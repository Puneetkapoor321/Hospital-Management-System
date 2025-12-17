from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Custom user with role field to distinguish doctors and patients."""

    ROLE_DOCTOR = "doctor"
    ROLE_PATIENT = "patient"

    ROLE_CHOICES = [
        (ROLE_DOCTOR, "Doctor"),
        (ROLE_PATIENT, "Patient"),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    def is_doctor(self) -> bool:
        return self.role == self.ROLE_DOCTOR

    def is_patient(self) -> bool:
        return self.role == self.ROLE_PATIENT


class DoctorProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="doctor_profile")
    specialization = models.CharField(max_length=100, blank=True)

    def __str__(self) -> str:
        return f"Dr. {self.user.get_full_name() or self.user.username}"


class PatientProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="patient_profile")
    date_of_birth = models.DateField(null=True, blank=True)

    def __str__(self) -> str:
        return self.user.get_full_name() or self.user.username
