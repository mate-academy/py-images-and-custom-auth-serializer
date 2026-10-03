"""Email account creation invariants."""
from django.contrib.auth import get_user_model
from django.test import TestCase


class EmailManagerTests(TestCase):
    def test_email_is_required(self) -> None:
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user("", "password")

    def test_normalizes_domain_and_hashes_password(self) -> None:
        user = get_user_model().objects.create_user(
            "buyer@EXAMPLE.COM", "password"
        )
        self.assertEqual(user.email, "buyer@example.com")
        self.assertTrue(user.check_password("password"))

    def test_superuser_flags_cannot_be_disabled(self) -> None:
        for flag in ("is_staff", "is_superuser"):
            with self.subTest(flag=flag), self.assertRaises(ValueError):
                get_user_model().objects.create_superuser(
                    "admin@example.com", "password", **{flag: False}
                )
