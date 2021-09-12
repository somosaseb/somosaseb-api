from django import forms
from django.contrib.auth.password_validation import validate_password
from django.db import transaction
from django.forms import widgets
from django.views.generic import FormView

from aseb.apps.users.models import User

from .constants import PHONE_CODES_CHOICES
from django.shortcuts import redirect


class RegisterForm(forms.Form):
    email = forms.EmailField(
        widget=widgets.EmailInput(
            attrs={
                "placeholder": "E-mail address",
                "autocomplete": "email",
            }
        )
    )

    password1 = forms.CharField(
        widget=widgets.PasswordInput,
        label="Password",
        min_length=8,
    )
    password2 = forms.CharField(
        widget=widgets.PasswordInput,
        label="Confirm password",
        min_length=8,
    )

    first_name = forms.CharField(max_length=140)
    last_name = forms.CharField(max_length=140)
    phone_country_code = forms.ChoiceField(
        choices=PHONE_CODES_CHOICES,
        initial="+591",
        required=False,
    )
    phone_number = forms.CharField(required=False)

    birthday = forms.DateField(
        required=False,
        widget=widgets.DateInput(
            attrs={"autocomplete": "off", "type": "date", "pattern": "\d{4}-\d{2}-\d{2}"}
        ),
    )

    def clean(self):
        cleaned_data = super().clean()
        cleaned_data["email"] = User.objects.normalize_email(self.cleaned_data["email"])

        if User.objects.filter(email__iexact=cleaned_data["email"]).exists():
            raise forms.ValidationError(
                {
                    "email": "A user is already registered with this e-mail address.",
                }
            )

        user = User(email=cleaned_data["email"])
        password1 = cleaned_data.pop("password1")
        password2 = cleaned_data.pop("password2")

        try:
            validate_password(password1, user)
        except forms.ValidationError as err:
            self.add_error("password1", err.message)

        if (password1 and password2) and password1 != password2:
            self.add_error("password2", "You must type the same password each time.")

        cleaned_data["password"] = password1

        return cleaned_data

    def save(self):
        data = self.cleaned_data
        birthday = data.pop("birthday")
        phone_country_code = data.pop("phone_country_code")
        phone_number = data.pop("phone_number")

        if phone_number:
            phone_number = f"{phone_country_code}{phone_number}"

        with transaction.atomic():
            user = User.objects.create_user(**data)

        return user


class RegisterView(FormView):
    form_class = RegisterForm
    template_name = "users/register.html"

    def form_valid(self, form):
        form.save()
        return redirect("/")
