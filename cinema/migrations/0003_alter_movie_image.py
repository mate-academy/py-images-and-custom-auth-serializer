# Generated by Django 4.1 on 2023-04-11 10:26

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("cinema", "0002_movie_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="movie",
            name="image",
            field=models.ImageField(null=True, upload_to="upload"),
        ),
    ]
