from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions
import firebase_admin
from firebase_admin import auth
from firebase_admin.exceptions import FirebaseError
from django.contrib.auth import get_user_model


class FirebaseAuthentication(BaseAuthentication):
    def authenticate(self, request):
        # Get the token from the Authorization header
        token = request.META.get('HTTP_AUTHORIZATION')

        if not token:
            return None

        try:
            # Verify the token and decode it
            token = token.replace('Bearer ', '', 1)  # Remove "Bearer " prefix if present
            # Uncomment these lines later after frontend sign in is created
            # decoded_token = auth.verify_id_token(token)
            # uid = decoded_token.get('uid')

            # Remove this line later after frontend sign in is created
            uid = token

        except ValueError:
            raise exceptions.AuthenticationFailed('Token is invalid')
        except FirebaseError:
            raise exceptions.AuthenticationFailed('Firebase auth error')

        # Here you have the option to check if the user exists in your db
        # You can create a user if it doesn't exist or update an existing user's info

        user = get_user_model().objects.get_or_create(username=uid)

        # Return the user and the token
        return (user, None)
