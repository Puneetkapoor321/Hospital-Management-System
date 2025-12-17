from django.http import JsonResponse
from django.shortcuts import redirect
from django.views.decorators.http import require_http_methods


@require_http_methods(["GET", "HEAD"])
def root_view(request):
    """Handle root URL for both HTML and JSON requests"""
    # Check if the request wants JSON/API response
    accept_header = request.META.get("HTTP_ACCEPT", "")
    
    # If request explicitly wants JSON or is from an API client
    if "application/json" in accept_header and "text/html" not in accept_header:
        # Return a simple API root response (no authentication required)
        return JsonResponse({
            "message": "Hospital Management System API",
            "version": "1.0",
            "endpoints": {
                "accounts": "/accounts/",
                "doctors": "/doctors/",
                "bookings": "/bookings/",
                "admin": "/admin/",
            }
        }, status=200)
    
    # For HTML requests (browser), redirect to landing page
    return redirect("accounts:landing")

