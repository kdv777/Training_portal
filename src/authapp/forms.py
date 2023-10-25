import os

from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.forms import ImageField, FileInput

from authapp.models import User


class UserRegisterForm(UserCreationForm):  # create user profile
    class Meta:
        model = User
        fields = ("username", "first_name", "password1", "password2", "email")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"
            field.help_text = ""


class UserLoginForm(AuthenticationForm):  # Authentication
    class Meta:
        model = User
        fields = ("username", "password")

    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"


class UserUpdateForm(forms.ModelForm):
    avatar = ImageField(widget=FileInput)

    class Meta:
        model = User
        fields = (
            "avatar",
            "first_name",
            "last_name",
            "email",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"

    def clean_avatar(self):
        arg_as_str = "avatar"
        if arg_as_str in self.changed_data and self.instance.avatar:
            if os.path.exists(self.instance.avatar.path):
                os.remove(self.instance.avatar.path)
        return self.cleaned_data.get(arg_as_str)
