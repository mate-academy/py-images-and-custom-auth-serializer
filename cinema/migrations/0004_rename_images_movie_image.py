# Generated by Django 4.2.7 on 2024-03-06 08:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cinema', '0003_rename_image_movie_images'),
    ]

    operations = [
        migrations.RenameField(
            model_name='movie',
            old_name='images',
            new_name='image',
        ),
    ]
