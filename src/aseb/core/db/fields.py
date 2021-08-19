from functools import partial
from uuid import uuid4

from django.db import models


class UUIDField(models.UUIDField):
    def get_pk_value_on_save(self, instance):
        return uuid4()


UUIDPrimaryKey = partial(UUIDField, primary_key=True, editable=False)
