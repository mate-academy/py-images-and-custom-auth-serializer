"""Upload permissions, storage naming, and nested image URLs."""
from __future__ import annotations

import tempfile
from io import BytesIO
from pathlib import Path
from uuid import UUID

from PIL import Image
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings
from django.utils import timezone
from rest_framework.test import APITestCase

from cinema.models import CinemaHall, Movie, MovieSession


class ImageSecurityTests(APITestCase):
    def setUp(self) -> None:
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        media = override_settings(MEDIA_ROOT=directory.name)
        media.enable()
        self.addCleanup(media.disable)
        self.user = get_user_model().objects.create_user(
            "buyer@example.com", "password"
        )
        self.client.force_authenticate(self.user)
        self.movie = Movie.objects.create(
            title="Space Adventure", description="A film", duration=90
        )
        self.url = f"/api/cinema/movies/{self.movie.pk}/upload-image/"

    def image(self) -> SimpleUploadedFile:
        content = BytesIO()
        Image.new("RGB", (4, 4)).save(content, format="PNG")
        return SimpleUploadedFile(
            "photo.png", content.getvalue(), content_type="image/png"
        )

    def test_regular_user_cannot_upload(self) -> None:
        response = self.client.post(
            self.url, {"image": self.image()}, format="multipart"
        )
        self.assertEqual(response.status_code, 403)
        self.movie.refresh_from_db()
        self.assertFalse(self.movie.image)

    def test_missing_image_is_rejected(self) -> None:
        self.user.is_staff = True
        self.user.save()
        response = self.client.post(self.url, {}, format="multipart")
        self.assertEqual(response.status_code, 400)

    def test_filename_and_nested_session_image(self) -> None:
        self.user.is_staff = True
        self.user.save()
        response = self.client.post(
            self.url, {"image": self.image()}, format="multipart"
        )
        self.assertEqual(response.status_code, 200)
        self.movie.refresh_from_db()
        filename = Path(self.movie.image.name)
        self.assertEqual(filename.suffix, ".png")
        self.assertTrue(filename.stem.startswith("space-adventure-"))
        UUID(filename.stem.removeprefix("space-adventure-"))
        hall = CinemaHall.objects.create(
            name="Blue", rows=10, seats_in_row=10
        )
        session = MovieSession.objects.create(
            movie=self.movie, cinema_hall=hall, show_time=timezone.now()
        )
        detail = self.client.get(
            f"/api/cinema/movie_sessions/{session.pk}/"
        )
        self.assertEqual(
            detail.data["movie"]["image"], response.data["image"]
        )
