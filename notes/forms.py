from django_registration.forms import RegistrationForm
from django.urls import reverse
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, ButtonHolder, HTML, Div

from . import models


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.form_action = reverse('login')
        self.helper.form_show_labels = False
        self.helper.layout = Layout(
            Div(
                HTML('<span class="input-group-text fas fa-user"></span>'),
                HTML('<input class="form-control" name="username" placeholder="Username">'),
                css_class='input-group mt-4'
            ),
            Div(
                HTML('<span class="input-group-text fas fa-lock"></span>'),
                HTML('<input class="form-control" type="password" name="password" placeholder="Password">'),
                css_class='input-group mt-3'
            ),
            ButtonHolder(Submit('submit', 'Log in'), css_class='mt-3')
        )


class SignupForm(forms.Form, RegistrationForm):
    username = forms.CharField()
    email = forms.CharField()
    password1 = forms.CharField()
    password2 = forms.CharField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.form_action = reverse('signup')
        self.helper.form_show_labels = False
        self.helper.layout = Layout(
            Div(
                HTML('<span class="input-group-text fas fa-user"></span>'),
                HTML('<input class="form-control" name="username" placeholder="Username">'),
                css_class='input-group mt-4'
            ),
            Div(
                HTML('<span class="input-group-text fas fa-envelope"></span>'),
                HTML('<input class="form-control" type="email" name="email" placeholder="Email">'),
                css_class='input-group mt-3'
            ),
            Div(
                HTML('<span class="input-group-text fas fa-lock"></span>'),
                HTML('<input class="form-control" type="password" name="password1" placeholder="Password">'),
                css_class='input-group mt-3'
            ),
            Div(
                HTML('<span class="input-group-text fas fa-lock"></span>'),
                HTML('<input class="form-control" type="password" name="password2" placeholder="Repeat password">'),
                css_class='input-group mt-3'
            ),
            ButtonHolder(Submit('submit', 'Sign up'), css_class='mt-3')
        )

    class Meta(RegistrationForm.Meta):
        model = models.User
