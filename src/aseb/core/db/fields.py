from functools import partial
from typing import Type
from uuid import uuid4

from django.core.exceptions import ValidationError
from django.db import models

from aseb.core.forms import PropertyForm


class UUIDField(models.UUIDField):
    def get_pk_value_on_save(self, instance):
        return uuid4()


UUIDPrimaryKey = partial(UUIDField, primary_key=True, editable=False)


class PropertiesField(models.JSONField):
    def __init__(
        self,
        form_class: Type[PropertyForm] = None,
        many: bool = False,
        *args,
        **kwargs,
    ):
        self.form_class = form_class or {}
        self.many = many
        kwargs.setdefault("default", list if many else dict)
        super().__init__(*args, **kwargs)

    def validate(self, value, model_instance):
        default_type = list if self.many else dict

        if not isinstance(value, default_type):
            raise ValidationError(
                f"Value {value!r} is not a {default_type!r}.",
                code="invalid_choice",
                params={"value": value},
            )

        values = value if self.many else [value]

        for n, item in enumerate(values):
            form = self.form_class(data=value)

            if not form.is_valid():
                raise ValidationError(
                    f"Value for item {n!r} is not not valid. {form.errors!r}"
                    if self.many
                    else f"Value is not not valid. {form.errors!r}",
                    code="invalid_choice",
                    params={"value": item},
                )

        super().validate(value, model_instance)
