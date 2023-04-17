# Generated by Django 4.1 on 2023-04-11 14:25

import cinema.models
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("cinema", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="movie",
            name="image",
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to=cinema.models.create_custom_path,
            ),
        ),
    ]
