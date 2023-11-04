from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User


class HashedPasswordAuthBackend(ModelBackend):

    def authenticate(self, username=None, password=None, **kwargs):
        try:
            return User.objects.get()
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get()
        except User.DoesNotExist:
            return None
