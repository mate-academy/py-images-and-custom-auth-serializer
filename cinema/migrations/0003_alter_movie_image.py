# Generated by Django 4.1 on 2023-08-03 14:50

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
            field=models.ImageField(null=True, upload_to=cinema.models.movie_image_file_path),
        ),
    ]
