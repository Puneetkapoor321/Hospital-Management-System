from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from .models import User, DoctorProfile, PatientProfile


class DoctorSignUpForm(UserCreationForm):
    specialization = forms.CharField(required=False)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ["username", "email", "first_name", "last_name"]

    def save(self, commit: bool = True) -> User:
        user: User = super().save(commit=False)
        user.role = User.ROLE_DOCTOR
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
            DoctorProfile.objects.create(
                user=user,
                specialization=self.cleaned_data.get("specialization", ""),
            )
        return user


class PatientSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ["username", "email", "first_name", "last_name"]

    def save(self, commit: bool = True) -> User:
        user: User = super().save(commit=False)
        user.role = User.ROLE_PATIENT
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
            PatientProfile.objects.create(user=user)
        return user


class LoginForm(AuthenticationForm):
    """Login by username or email."""

    username = forms.CharField(label="Username or Email")

    def clean(self):
        # Allow login by email or username
        username = self.cleaned_data.get("username")
        from django.contrib.auth import get_user_model

        UserModel = get_user_model()
        if username:
            try:
                user_obj = UserModel.objects.get(email__iexact=username)
                self.cleaned_data["username"] = user_obj.username
            except UserModel.DoesNotExist:
                # Fall back to username login
                pass
        return super().clean()
