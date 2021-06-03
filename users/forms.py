from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UsernameField

User = get_user_model()


class CreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "first_name", "last_name", "email")
        field_classes = {"username": UsernameField}

    def __init__(self, *args, **kwargs):
        super(CreationForm, self).__init__(*args, **kwargs)
        self.fields["email"].required = True
