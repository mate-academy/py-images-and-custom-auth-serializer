# Generated by Django 4.1 on 2024-03-20 13:05

import cinema.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cinema', '0002_movie_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='image',
            field=models.ImageField(null=True, upload_to=cinema.models.movies),
        ),
    ]
