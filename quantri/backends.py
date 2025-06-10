from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

User = get_user_model()

class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        email = kwargs.get('email', username)
        users = User.objects.filter(email=email)
        for user in users:
            if user.check_password(password):
                return user
        return None
