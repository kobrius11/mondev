from django.contrib.auth import get_user_model
from django import forms
from . import models


User = get_user_model()


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ("first_name", "last_name", "username", "email")


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = models.Profile
        fields = ("picture",)


class SignupForm(forms.ModelForm):
    password_confirm = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ("first_name", "last_name", "username", "email", "password")

    def clean_password_confirm(self):
        password = self.cleaned_data.get('password')
        password_confirm = self.cleaned_data.get('password_confirm')

        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Password must match.")
        return password_confirm
