import io
import tempfile
from pathlib import Path
from uuid import UUID

from PIL import Image
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from cinema.models import CinemaHall, Movie, MovieSession


class ImageRequirementsTests(TestCase):
    def setUp(self) -> None:
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        settings = self.settings(MEDIA_ROOT=directory.name)
        settings.enable()
        self.addCleanup(settings.disable)
        self.client = APIClient()
        self.staff = get_user_model().objects.create_superuser(
            email="staff@example.com", password="password"
        )
        self.client.force_authenticate(self.staff)
        self.movie = Movie.objects.create(
            title="A Sample Movie!", description="Description", duration=90
        )
        hall = CinemaHall.objects.create(name="Blue", rows=2, seats_in_row=3)
        self.session = MovieSession.objects.create(
            movie=self.movie, cinema_hall=hall, show_time="2026-10-20T12:00:00"
        )
        self.url = reverse("cinema:movie-upload-image", args=[self.movie.pk])

    @staticmethod
    def image() -> SimpleUploadedFile:
        content = io.BytesIO()
        Image.new("RGB", (10, 10)).save(content, format="JPEG")
        return SimpleUploadedFile(
            "photo.jpg", content.getvalue(), content_type="image/jpeg"
        )

    def test_filename_and_all_read_representations(self) -> None:
        response = self.client.post(
            self.url, {"image": self.image()}, format="multipart"
        )
        self.assertEqual(response.status_code, 200)
        self.movie.refresh_from_db()
        path = Path(self.movie.image.name)
        self.assertEqual(path.parent.as_posix(), "uploads/movies")
        self.assertEqual(path.suffix, ".jpg")
        UUID(path.stem.removeprefix("a-sample-movie-"))
        self.assertTrue(path.stem.startswith("a-sample-movie-"))
        image_url = response.data["image"]
        self.assertTrue(image_url.startswith("http://testserver/media/"))
        response = self.client.get(reverse("cinema:movie-list"))
        self.assertEqual(response.data[0]["image"], image_url)
        response = self.client.get(
            reverse("cinema:movie-detail", args=[self.movie.pk])
        )
        self.assertEqual(response.data["image"], image_url)
        response = self.client.get(reverse("cinema:moviesession-list"))
        self.assertEqual(response.data[0]["movie_image"], image_url)
        response = self.client.get(
            reverse("cinema:moviesession-detail", args=[self.session.pk])
        )
        self.assertEqual(response.data["movie"]["image"], image_url)

    def test_upload_requires_staff(self) -> None:
        self.client.force_authenticate(None)
        self.assertEqual(
            self.client.post(
                self.url, {"image": self.image()}, format="multipart"
            ).status_code, 401
        )
        user = get_user_model().objects.create_user(
            email="user@example.com", password="password"
        )
        self.client.force_authenticate(user)
        self.assertEqual(
            self.client.post(
                self.url, {"image": self.image()}, format="multipart"
            ).status_code, 403
        )
        self.movie.refresh_from_db()
        self.assertFalse(self.movie.image)

    def test_missing_image_is_rejected(self) -> None:
        response = self.client.post(self.url, {}, format="multipart")
        self.assertEqual(response.status_code, 400)
        self.movie.refresh_from_db()
        self.assertFalse(self.movie.image)
