from typing import Any

from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, ButtonHolder, Div, Layout, Submit
from django.contrib.auth.forms import AuthenticationForm
from django_registration.forms import RegistrationForm

from . import models


class InputBuilder:
    def __init__(self, name, type, placeholder, icon):
        self.placeholder = placeholder
        self.name = name
        self.type = type
        self.icon = icon

    def build(self):
        return Div(
            HTML(f'<input class="form-control" type="{self.type}" name="{self.name}"\
                    id="{self.name}-input" placeholder="{self.placeholder}">'),
            HTML(f'<label for="{self.name}-input">\
                    <span class="bi fas {self.icon} me-2"></span>{self.placeholder}\
                    </label>'),
            css_class='form-floating text-dark my-4'
        )


class LoginForm(AuthenticationForm):
    def __init__(self, request: Any, *args: Any, **kwargs: Any) -> None:
        super().__init__(request=request, *args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            InputBuilder('username', 'username', 'Username', 'fa-user').build(),
            InputBuilder('password', 'password', 'Password', 'fa-lock').build(),
            ButtonHolder(Submit('submit', 'Log in'), css_class='mt-3'),
        )


class SignupForm(RegistrationForm):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            InputBuilder('username', 'username', 'Username', 'fa-user').build(),
            InputBuilder('email', 'email', 'Email address', 'fa-envelope').build(),
            InputBuilder('password1', 'password', 'Password', 'fa-lock').build(),
            InputBuilder('password2', 'password', 'Password confirmation', 'fa-lock').build(),
            ButtonHolder(Submit('submit', 'Sign up'), css_class='mt-3'),
        )

    class Meta(RegistrationForm.Meta):
        model = models.User
