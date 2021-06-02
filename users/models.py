from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, ValidationError


User = get_user_model()


class CreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("first_name", "username", "email", "password1")
