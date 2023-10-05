
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
# from django.contrib.auth.base_user import AbstractBaseUser
# from django.http.request import HttpRequest



class CheckUser(ModelBackend):
    def authenticate(self,username=None, password=None, **kwargs):
        UserModel=get_user_model()
        try:
            if username.endswith('.com'):
                user=UserModel.objects.get(email=username)
            else:
                user=UserModel.objects.get(phone_number=username)
        except UserModel.DoesNotExist as e:
            return None

        else:
            if user.check_password(password):
                return user
        return None