import os
from uuid import uuid4
from django.utils.deconstruct import deconstructible
from django.utils.text import slugify
from django.db.models import base


@deconstructible
class UploadToFunction:
    def __init__(self, format_string: str):
        assert "{ext}" in format_string, "Missing filename extension placeholder"

        self.format_string = format_string

    def __call__(self, instance: base.Model, filename: str) -> str:
        filename, ext = os.path.splitext(filename)
        filename = slugify(filename)
        ext = ext.strip(".")
        uuid_hex = uuid4()
        model_name = instance.__class__._meta.model_name

        return self.format_string.format(
            obj=instance,
            filename=filename,
            ext=ext,
            model_name=model_name,
            uuid=uuid_hex,
        )
