# Generated by Django 4.0.4 on 2022-07-19 06:25

import cinema.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cinema', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='image',
            field=models.ImageField(null=True, upload_to=cinema.models.movie_image_file_path),
        ),
    ]
