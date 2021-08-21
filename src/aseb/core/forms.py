from typing import TypeVar

from django import forms

from aseb.core.db.models.base import BaseModel

ModelT = TypeVar("ModelT", bound=BaseModel)


class PropertyForm(forms.Form):
    def __init__(self, *args, model_instance: ModelT, **kwargs):
        self.model_instance = model_instance
        super().__init__(*args, **kwargs)


class ContactForm(PropertyForm):
    contact_email = forms.EmailField(required=False)
    contact_phone = forms.CharField(required=False)

    location_country = forms.CharField(required=False, max_length=100)
    location_city = forms.CharField(required=False, max_length=100)

    link_facebook = forms.CharField(required=False, max_length=200)
    link_instagram = forms.CharField(required=False, max_length=200)
    link_linkedIn = forms.CharField(required=False, max_length=200)
    link_website = forms.CharField(required=False, max_length=200)
    link_twitter = forms.CharField(required=False, max_length=200)
