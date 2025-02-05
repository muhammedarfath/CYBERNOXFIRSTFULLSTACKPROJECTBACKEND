from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model

User = get_user_model()

class EmailOrMobileBackend(BaseBackend):
    def authenticate(self, request, email=None, mobileno=None, password=None):
        try:
            if email:
                user = User.objects.get(email=email)
            elif mobileno:
                user = User.objects.get(mobileno=mobileno)
            else:
                return None
        except User.DoesNotExist:
            return None

        if user.check_password(password):
            return user
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
