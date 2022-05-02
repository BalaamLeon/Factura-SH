from django.contrib.auth.forms import UserCreationForm

from apps.base.models.customuser import CustomUser


class RegisterForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ("username", "email", "password1", "password2")