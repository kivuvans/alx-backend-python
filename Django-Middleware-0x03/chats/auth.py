from rest_framework_simplejwt.authentication import JWTAuthentication


class CustomJWTAuthentication(JWTAuthentication):
    """
    Extends default JWTAuthentication if you want to customize later.
    Currently just uses default behavior.
    """
    pass
