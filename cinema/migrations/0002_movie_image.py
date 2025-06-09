from django.db import migrations, models
import uuid


def movie_image_file_path_stub(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return f"uploads/movies/{filename}"


class Migration(migrations.Migration):

    dependencies = [
        ("cinema", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="movie",
            name="image",
            field=models.ImageField(
                null=True,
                upload_to=movie_image_file_path_stub
            ),
        ),
    ]
