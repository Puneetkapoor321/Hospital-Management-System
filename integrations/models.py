from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class GoogleCredentials(models.Model):
    """Stores serialized Google OAuth2 credentials JSON for a user."""

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="google_credentials")
    credentials_json = models.TextField()

    def __str__(self) -> str:
        return f"Google credentials for {self.user}"
