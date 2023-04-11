# Generated by Django 4.1 on 2023-04-11 17:33

import cinema.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("cinema", "0003_movie_image_delete_image"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="movie",
            name="image",
        ),
        migrations.CreateModel(
            name="Image",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("image", models.ImageField(upload_to=cinema.models.create_image_path)),
                (
                    "movie",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="images",
                        to="cinema.movie",
                    ),
                ),
            ],
        ),
    ]