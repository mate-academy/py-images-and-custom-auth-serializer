# Generated by Django 4.1 on 2022-12-27 14:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("cinema", "0002_movie_movie_image"),
    ]

    operations = [
        migrations.RenameField(
            model_name="movie",
            old_name="movie_image",
            new_name="image",
        ),
    ]
