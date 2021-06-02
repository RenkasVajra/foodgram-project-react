from django import forms
from django.contrib.auth.forms import UserCreationForm, ValidationError

from .models import User


class UserRegistrationForm(forms.ModelForm):
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput
    )
    password2 = forms.CharField(
        label="Repeat password",
        widget=forms.PasswordInput
    )
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("first_name", "username", "email", "password1")

    def clean_password2(self):
        cd = self.cleaned_data
        if cd["password1"] != cd["password2"]:
            raise forms.ValidationError("Пароли не совпадают!")
        return cd["password2"]

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError(
                "Пользователь с такой почтой уже зарегистрирован"
            )
        return email
