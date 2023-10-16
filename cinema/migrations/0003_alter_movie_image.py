# Generated by Django 4.1 on 2023-10-16 21:06

import cinema.models
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("cinema", "0002_movie_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="movie",
            name="image",
            field=models.ImageField(
                null=True, upload_to=cinema.models.create_movie_image_path
            ),
        ),
    ]
