import os

from io import BytesIO
from pathlib import Path
from tempfile import TemporaryDirectory
from uuid import UUID

from PIL import Image
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import models
from django.test import SimpleTestCase, TestCase, override_settings
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from cinema.models import Actor, CinemaHall, Genre, Movie, MovieSession


def movie_image_file(name="poster.cover.JPEG"):
    buffer = BytesIO()
    Image.new("RGB", (12, 8), color="blue").save(buffer, format="JPEG")
    return SimpleUploadedFile(
        name, buffer.getvalue(), content_type="image/jpeg"
    )


class MovieImageModelTests(SimpleTestCase):
    def test_movie_image_is_optional(self):
        field_names = {field.name for field in Movie._meta.get_fields()}
        self.assertIn("image", field_names)

        image_field = Movie._meta.get_field("image")
        self.assertIsInstance(image_field, models.ImageField)
        self.assertTrue(image_field.blank)
        self.assertFalse(Movie(title="Without a poster").image)

    def test_image_filename_uses_title_uuid4_and_original_extension(self):
        movie = Movie(title="The Big Movie: Part 2!")
        image_field = Movie._meta.get_field("image")

        first_name = image_field.generate_filename(movie, "poster.cover.JPEG")
        second_name = image_field.generate_filename(movie, "poster.cover.JPEG")

        first_path = Path(first_name)
        self.assertEqual(first_path.parent, Path("uploads/movies"))
        self.assertEqual(first_path.suffix, ".JPEG")
        self.assertTrue(first_path.stem.startswith("the-big-movie-part-2-"))
        identifier = UUID(
            first_path.stem.removeprefix("the-big-movie-part-2-")
        )
        self.assertEqual(identifier.version, 4)
        self.assertEqual(str(identifier), str(identifier).lower())
        self.assertNotEqual(first_name, second_name)

    def test_upload_image_url_is_registered(self):
        self.assertEqual(
            reverse("cinema:movie-upload-image", args=[42]),
            "/api/cinema/movies/42/upload-image/",
        )


class MovieImageApiTests(TestCase):
    def setUp(self):
        media_parent = os.path.abspath(settings.BASE_DIR)
        if os.name == "nt":
            media_parent = "\\\\?\\" + media_parent
        media_directory = TemporaryDirectory(dir=media_parent)
        self.addCleanup(media_directory.cleanup)
        media_override = override_settings(MEDIA_ROOT=media_directory.name)
        media_override.enable()
        self.addCleanup(media_override.disable)

        user_model = get_user_model()
        self.staff = user_model.objects.create_user(
            **{user_model.USERNAME_FIELD: "staff@example.com"},
            password="test-password",
            is_staff=True,
        )
        self.client = APIClient()
        token = Token.objects.create(user=self.staff)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
        self.movie = Movie.objects.create(
            title="The Big Movie: Part 2!",
            description="A sample movie",
            duration=90,
        )
        cinema_hall = CinemaHall.objects.create(
            name="Blue", rows=10, seats_in_row=12
        )
        self.movie_session = MovieSession.objects.create(
            movie=self.movie,
            cinema_hall=cinema_hall,
            show_time=timezone.now(),
        )

    def upload_url(self, movie_id=None):
        return reverse(
            "cinema:movie-upload-image",
            args=[movie_id if movie_id is not None else self.movie.pk],
        )

    def store_image(self):
        self.movie.image.save("poster.jpeg", movie_image_file("poster.jpeg"))
        return f"http://testserver{self.movie.image.url}"

    def assert_uploaded_image_name(self, title, expected_slug):
        self.movie.title = title
        self.movie.save(update_fields=["title"])
        image_file = movie_image_file()
        expected_content = image_file.read()
        image_file.seek(0)

        response = self.client.post(
            self.upload_url(), {"image": image_file}, format="multipart"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.movie.refresh_from_db()
        stored_path = Path(self.movie.image.name)
        self.assertEqual(stored_path.parent, Path("uploads/movies"))
        self.assertEqual(stored_path.suffix, ".JPEG")
        self.assertTrue(stored_path.stem.startswith(f"{expected_slug}-"))
        identifier_text = stored_path.stem.removeprefix(f"{expected_slug}-")
        identifier = UUID(identifier_text)
        self.assertEqual(identifier.version, 4)
        self.assertEqual(identifier_text, str(identifier))
        self.assertEqual(self.movie.title, title)
        with self.movie.image.open("rb") as stored_image:
            self.assertEqual(stored_image.read(), expected_content)
        return self.movie.image.name

    def test_upload_preserves_full_slug_for_80_character_title(self):
        self.assert_uploaded_image_name("A" * 80, "a" * 80)

    def test_upload_shortens_only_slug_for_255_character_title(self):
        stored_name = self.assert_uploaded_image_name("A" * 255, "a" * 198)

        self.assertEqual(len(stored_name), 255)
        self.assertEqual(Movie._meta.get_field("image").max_length, 255)

    def test_upload_handles_unicode_title_that_expands_when_slugified(self):
        stored_name = self.assert_uploaded_image_name("ﬃ" * 100, "ffi" * 66)

        self.assertEqual(len(stored_name), 255)

    def test_staff_uploads_valid_image_and_saves_original_content(self):
        image_file = movie_image_file()
        expected_content = image_file.read()
        image_file.seek(0)

        response = self.client.post(
            self.upload_url(), {"image": image_file}, format="multipart"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.movie.refresh_from_db()
        self.assertEqual(
            response.data["image"],
            f"http://testserver{self.movie.image.url}",
        )
        with self.movie.image.open("rb") as stored_image:
            self.assertEqual(stored_image.read(), expected_content)
        with Image.open(self.movie.image.path) as stored_image:
            self.assertEqual(stored_image.format, "JPEG")
            self.assertEqual(stored_image.size, (12, 8))

    def test_upload_rejects_non_image_file(self):
        invalid_file = SimpleUploadedFile(
            "poster.jpeg", b"this is not an image", content_type="image/jpeg"
        )

        response = self.client.post(
            self.upload_url(), {"image": invalid_file}, format="multipart"
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("image", response.data)
        self.movie.refresh_from_db()
        self.assertFalse(self.movie.image)

    def test_upload_requires_image(self):
        response = self.client.post(self.upload_url(), {}, format="multipart")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("image", response.data)
        self.movie.refresh_from_db()
        self.assertFalse(self.movie.image)

    def test_upload_rejects_null_and_keeps_existing_image(self):
        self.store_image()
        original_name = self.movie.image.name

        response = self.client.post(
            self.upload_url(), {"image": None}, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("image", response.data)
        self.movie.refresh_from_db()
        self.assertEqual(self.movie.image.name, original_name)
        self.assertTrue(self.movie.image.storage.exists(original_name))

    def test_upload_missing_movie_returns_404(self):
        response = self.client.post(
            self.upload_url(self.movie.pk + 1),
            {"image": movie_image_file()},
            format="multipart",
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_movie_creation_ignores_image(self):
        genre = Genre.objects.create(name="Drama")
        actor = Actor.objects.create(first_name="Sample", last_name="Actor")
        response = self.client.post(
            reverse("cinema:movie-list"),
            {
                "title": "Created without a poster",
                "description": "A movie from the regular create endpoint",
                "duration": 95,
                "genres": [genre.pk],
                "actors": [actor.pk],
                "image": movie_image_file(),
            },
            format="multipart",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        movie = Movie.objects.get(pk=response.data["id"])
        self.assertFalse(movie.image)

    def test_movie_list_contains_image_url(self):
        expected_url = self.store_image()

        response = self.client.get(reverse("cinema:movie-list"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["image"], expected_url)

    def test_movie_detail_contains_image_url(self):
        expected_url = self.store_image()

        response = self.client.get(
            reverse("cinema:movie-detail", args=[self.movie.pk])
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["image"], expected_url)

    def test_movie_session_list_contains_movie_image_url(self):
        expected_url = self.store_image()

        response = self.client.get(reverse("cinema:moviesession-list"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["movie_image"], expected_url)

    def test_movie_session_detail_contains_nested_movie_image_url(self):
        expected_url = self.store_image()

        response = self.client.get(
            reverse("cinema:moviesession-detail", args=[self.movie_session.pk])
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["movie"]["image"], expected_url)

    def test_session_list_reflects_image_uploaded_after_previous_get(self):
        first_response = self.client.get(reverse("cinema:moviesession-list"))
        self.assertEqual(first_response.status_code, status.HTTP_200_OK)
        self.assertIsNone(first_response.data[0]["movie_image"])

        upload_response = self.client.post(
            self.upload_url(),
            {"image": movie_image_file()},
            format="multipart",
        )
        self.assertEqual(upload_response.status_code, status.HTTP_200_OK)

        second_response = self.client.get(reverse("cinema:moviesession-list"))

        self.assertEqual(second_response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            second_response.data[0]["movie_image"],
            upload_response.data["image"],
        )

    def test_movies_without_images_return_null_on_all_read_endpoints(self):
        movie_list = self.client.get(reverse("cinema:movie-list"))
        movie_detail = self.client.get(
            reverse("cinema:movie-detail", args=[self.movie.pk])
        )
        session_list = self.client.get(reverse("cinema:moviesession-list"))
        session_detail = self.client.get(
            reverse("cinema:moviesession-detail", args=[self.movie_session.pk])
        )

        for response in (
            movie_list, movie_detail, session_list, session_detail
        ):
            self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNone(movie_list.data[0]["image"])
        self.assertIsNone(movie_detail.data["image"])
        self.assertIsNone(session_list.data[0]["movie_image"])
        self.assertIsNone(session_detail.data["movie"]["image"])

    def test_anonymous_user_cannot_upload_image(self):
        self.client.credentials()

        response = self.client.post(
            self.upload_url(),
            {"image": movie_image_file()},
            format="multipart",
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.movie.refresh_from_db()
        self.assertFalse(self.movie.image)

    def test_regular_user_cannot_upload_image(self):
        user_model = get_user_model()
        regular_user = user_model.objects.create_user(
            **{user_model.USERNAME_FIELD: "reader@example.com"},
            password="test-password",
        )
        token = Token.objects.create(user=regular_user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

        response = self.client.post(
            self.upload_url(),
            {"image": movie_image_file()},
            format="multipart",
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.movie.refresh_from_db()
        self.assertFalse(self.movie.image)

    def test_regular_user_can_read_movie_image(self):
        expected_url = self.store_image()
        user_model = get_user_model()
        regular_user = user_model.objects.create_user(
            **{user_model.USERNAME_FIELD: "reader@example.com"},
            password="test-password",
        )
        token = Token.objects.create(user=regular_user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

        response = self.client.get(
            reverse("cinema:movie-detail", args=[self.movie.pk])
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["image"], expected_url)

    def test_anonymous_user_cannot_read_movie_images(self):
        self.client.credentials()

        response = self.client.get(reverse("cinema:movie-list"))

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
