from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient


class EmailRequirementsTests(TestCase):
    def test_manager_normalizes_email_and_hashes_password(self) -> None:
        user = get_user_model().objects.create_user(
            "person@EXAMPLE.COM", "password"
        )
        self.assertEqual(user.email, "person@example.com")
        self.assertTrue(user.check_password("password"))
        self.assertEqual(user.USERNAME_FIELD, "email")
        self.assertNotIn("username", [f.name for f in user._meta.fields])

    def test_manager_rejects_missing_email_and_invalid_staff_flags(self):
        manager = get_user_model().objects
        with self.assertRaises(ValueError):
            manager.create_user("", "password")
        with self.assertRaises(ValueError):
            manager.create_superuser(
                "staff@example.com", "password", is_staff=False
            )
        with self.assertRaises(ValueError):
            manager.create_superuser(
                "staff@example.com", "password", is_superuser=False
            )

    def test_email_token_authentication_and_inactive_user(self) -> None:
        user = get_user_model().objects.create_user(
            "person@example.com", "password"
        )
        client = APIClient()
        response = client.post(
            reverse("user:login"),
            {"email": user.email, "password": "password"},
        )
        self.assertEqual(response.status_code, 200)
        client.credentials(
            HTTP_AUTHORIZATION=f"Token {response.data['token']}"
        )
        self.assertEqual(client.get(reverse("user:manage")).status_code, 200)
        user.is_active = False
        user.save()
        self.assertEqual(client.get(reverse("user:manage")).status_code, 401)
        client.credentials()
        response = client.post(
            reverse("user:login"),
            {"email": user.email, "password": "password"},
        )
        self.assertEqual(response.status_code, 400)

    def test_admin_add_user_form_works_with_email(self) -> None:
        user = get_user_model().objects.create_superuser(
            "staff@example.com", "password"
        )
        self.client.force_login(user)
        response = self.client.get(reverse("admin:user_user_add"))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(
            reverse("admin:user_user_add"),
            {
                "email": "new@example.com",
                "password1": "Str0ng-admin-password-391",
                "password2": "Str0ng-admin-password-391",
                "_save": "Save",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            get_user_model().objects.filter(email="new@example.com").exists()
        )
