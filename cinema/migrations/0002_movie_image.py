# Generated by Django 4.1 on 2024-03-19 19:07

import cinema.helpers
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cinema', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=cinema.helpers.create_custom_path),
        ),
    ]
