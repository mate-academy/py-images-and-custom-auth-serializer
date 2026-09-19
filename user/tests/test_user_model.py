from django.contrib.auth import authenticate, get_user_model
from django.core.exceptions import FieldDoesNotExist
from django.test import TestCase


class UserModelTests(TestCase):
    def test_create_user_with_email_and_password(self):
        user = get_user_model().objects.create_user(
            email="Test@EXAMPLE.COM", password="testpass123"
        )

        self.assertEqual(user.email, "Test@example.com")
        self.assertTrue(user.check_password("testpass123"))
        self.assertNotEqual(user.password, "testpass123")
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertEqual(
            authenticate(email=user.email, password="testpass123"), user
        )
        self.assertEqual(user.USERNAME_FIELD, "email")
        self.assertEqual(user.REQUIRED_FIELDS, [])
        with self.assertRaises(FieldDoesNotExist):
            user._meta.get_field("username")

    def test_create_user_without_email(self):
        for email in (None, ""):
            with self.subTest(email=email):
                with self.assertRaisesMessage(
                    ValueError, "The given email must be set"
                ):
                    get_user_model().objects.create_user(
                        email=email, password="testpass123"
                    )

    def test_create_superuser(self):
        user = get_user_model().objects.create_superuser(
            email="admin@example.com", password="testpass123"
        )

        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.check_password("testpass123"))

    def test_create_superuser_rejects_invalid_flags(self):
        for flag in ("is_staff", "is_superuser"):
            with self.subTest(flag=flag):
                with self.assertRaisesMessage(
                    ValueError, f"Superuser must have {flag}=True."
                ):
                    get_user_model().objects.create_superuser(
                        email="admin@example.com",
                        password="testpass123",
                        **{flag: False},
                    )
