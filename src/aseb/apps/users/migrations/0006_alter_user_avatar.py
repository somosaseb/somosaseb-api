# Generated by Django 3.2.6 on 2021-08-25 23:27

import aseb.core.db.utils
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0005_alter_accesstoken_expires"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="avatar",
            field=models.ImageField(
                blank=True, upload_to=aseb.core.db.utils.UploadToFunction("avatars/{uuid}.{ext}")
            ),
        ),
    ]
