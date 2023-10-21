from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

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
