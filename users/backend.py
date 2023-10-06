from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

from .models import User

UserModel = get_user_model()
 # Project specific implementation of authentication to provide for email auth
class EmailBackend(ModelBackend):
    def authenticate(self, request=None, telephone = None, password = None, **kwargs):
        if telephone is None or password is None:
            return
        try:
            user = User.objects.get(email=telephone)
        except UserModel.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a nonexistent user (#20760).
            UserModel().set_password(password)
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user

