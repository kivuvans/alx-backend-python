from datetime import datetime, timedelta
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseTooManyRequests
from django.http import HttpResponseForbidden
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class RequestLoggingMiddleware:
    """
    Middleware that logs each user request with:
    - timestamp
    - username or AnonymousUser
    - request path
    """

    def __init__(self, get_response):
        self.get_response = get_response

        # Configure a file logger
        logging.basicConfig(
            filename="requests.log",
            level=logging.INFO,
            format="%(message)s"
        )

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else "AnonymousUser"

        log_message = f"{datetime.now()} - User: {user} - Path: {request.path}"
        logger.info(log_message)

        response = self.get_response(request)
        return response


class RestrictAccessByTimeMiddleware:
    """
    Middleware blocks access to the chat system
    outside allowed hours (6AM – 9PM).
    If current time is NOT between 6AM and 9PM → return 403 Forbidden.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_hour = datetime.now().hour

        # Allowed hours: 6AM (06:00) to 9PM (21:00)
        if not (6 <= current_hour < 21):
            return HttpResponseForbidden(
                "Access to chat is restricted between 9PM and 6AM."
            )

        return self.get_response(request)


class OffensiveLanguageMiddleware:
    """
    Middleware that rate-limits users by IP.
    Each IP can only send 5 POST (message) requests per 1-minute window.
    """

    def __init__(self, get_response):
        self.get_response = get_response
        # Structure: { "ip": [timestamp1, timestamp2, ...] }
        self.requests_log = {}

    def __call__(self, request):
        ip = request.META.get("REMOTE_ADDR")
        now = datetime.now()

        # Only limit POST requests (sending messages)
        if request.method == "POST":
            if ip not in self.requests_log:
                self.requests_log[ip] = []

            # Remove timestamps older than 1 minute
            one_minute_ago = now - timedelta(minutes=1)
            self.requests_log[ip] = [
                ts for ts in self.requests_log[ip] if ts > one_minute_ago
            ]

            # Check limit (5 per minute)
            if len(self.requests_log[ip]) >= 5:
                return HttpResponseTooManyRequests(
                    "Rate limit exceeded: Only 5 messages allowed per minute."
                )

            # Log new request
            self.requests_log[ip].append(now)

        return self.get_response(request)


class RolePermissionMiddleware:
    """
    Middleware that allows only users with specific roles (admin or moderator)
    to access protected endpoints.
    """

    ALLOWED_ROLES = ["admin", "moderator"]

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        # Ignore admin dashboard and authentication routes
        if request.path.startswith("/admin/"):
            return self.get_response(request)

        # Only perform role checking if user is authenticated
        user = request.user
        if user.is_authenticated:
            # custom field from your User model
            role = getattr(user, "role", None)

            # If user role is not allowed, block the request
            if role not in self.ALLOWED_ROLES:
                return HttpResponseForbidden(
                    "Access denied: You do not have permission to access this resource."
                )
        else:
            # Not authenticated → automatically blocked
            return HttpResponseForbidden("User must be authenticated.")

        return self.get_response(request)
