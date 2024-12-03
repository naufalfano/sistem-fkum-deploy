from django.shortcuts import redirect
from django.conf import settings

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Paths that do not require authentication
        allowed_paths = [
            settings.LOGIN_URL,  # Default login page
        ]

        # Redirect if the user is not authenticated and the path is not allowed
        if not request.user.is_authenticated and request.path not in allowed_paths:
            return redirect(settings.LOGIN_URL)

        # Process the request
        return self.get_response(request)
