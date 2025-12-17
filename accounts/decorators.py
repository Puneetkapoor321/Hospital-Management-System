from functools import wraps

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden


def role_required(role: str):
    """Decorator enforcing a specific user role."""

    def decorator(view_func):
        @login_required
        @wraps(view_func)
        def _wrapped(request, *args, **kwargs):
            if getattr(request.user, "role", None) != role:
                return HttpResponseForbidden("You do not have permission to access this page.")
            return view_func(request, *args, **kwargs)

        return _wrapped

    return decorator


def doctor_required(view_func):
    from .models import User

    return role_required(User.ROLE_DOCTOR)(view_func)


def patient_required(view_func):
    from .models import User

    return role_required(User.ROLE_PATIENT)(view_func)
