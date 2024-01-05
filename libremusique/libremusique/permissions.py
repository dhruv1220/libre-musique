from rest_framework import permissions
from firebase_admin import auth

class FirebasePermission(permissions.BasePermission):
    """
    Custom permission to only allow access to authenticated Firebase users.
    """

    def has_permission(self, request, view):
        # Assuming the Firebase token is passed in the Authorization header
        token = request.META.get('HTTP_AUTHORIZATION')
        if not token:
            return False

        try:
            # Verify the Firebase token
            # Uncomment these 2 lines later once sign in functionality is added
            # decoded_token = auth.verify_id_token(token)
            # request.user = decoded_token
            return True
        except Exception:
            return False
