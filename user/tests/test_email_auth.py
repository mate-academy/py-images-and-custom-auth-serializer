from django.contrib.auth import get_user_model
from django.core.exceptions import FieldDoesNotExist
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APIRequestFactory

from user import serializers as user_serializers


REGISTER_URL = reverse("user:create")
LOGIN_URL = reverse("user:login")
PROFILE_URL = reverse("user:manage")


class EmailUserModelTests(TestCase):
    def test_email_is_required_unique_login_field(self):
        user_model = get_user_model()
        email_field = user_model._meta.get_field("email")

        self.assertEqual(user_model.USERNAME_FIELD, "email")
        self.assertEqual(user_model.REQUIRED_FIELDS, [])
        self.assertTrue(email_field.unique)
        self.assertFalse(email_field.blank)
        with self.assertRaises(FieldDoesNotExist):
            user_model._meta.get_field("username")

    def test_create_user_accepts_email_and_password_positionally(self):
        user = get_user_model().objects.create_user(
            "Member@EXAMPLE.COM", "secret-password"
        )

        self.assertEqual(user.email, "Member@example.com")
        self.assertTrue(user.check_password("secret-password"))
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_user_without_password_has_unusable_password(self):
        self.assertEqual(get_user_model().USERNAME_FIELD, "email")

        user = get_user_model().objects.create_user("member@example.com")

        self.assertEqual(user.email, "member@example.com")
        self.assertFalse(user.has_usable_password())

    def test_create_user_rejects_missing_email(self):
        manager = get_user_model().objects

        for email in (None, ""):
            with self.subTest(email=email):
                with self.assertRaises(ValueError):
                    manager.create_user(email, "secret-password")

    def test_create_superuser_accepts_email_and_password_positionally(self):
        self.assertEqual(get_user_model().USERNAME_FIELD, "email")

        user = get_user_model().objects.create_superuser(
            "Admin@EXAMPLE.COM", "secret-password"
        )

        self.assertEqual(user.email, "Admin@example.com")
        self.assertTrue(user.check_password("secret-password"))
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

    def test_create_superuser_rejects_disabled_privileges(self):
        manager = get_user_model().objects

        for flag in ("is_staff", "is_superuser"):
            with self.subTest(flag=flag):
                with self.assertRaises(ValueError):
                    manager.create_superuser(
                        "admin@example.com",
                        "secret-password",
                        **{flag: False},
                    )


class EmailAuthenticationApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.client.raise_request_exception = False
        self.user = get_user_model()(email="member@example.com")
        self.user.set_password("secret-password")
        self.user.save()

    def test_registration_normalizes_email_and_hashes_password(self):
        response = self.client.post(
            REGISTER_URL,
            {
                "email": "NewMember@EXAMPLE.COM",
                "password": "secret-password",
                "is_staff": True,
                "is_superuser": True,
            },
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(pk=response.data["id"])
        self.assertEqual(user.email, "NewMember@example.com")
        self.assertTrue(user.check_password("secret-password"))
        self.assertNotEqual(user.password, "secret-password")
        self.assertNotIn("password", response.data)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_registration_rejects_duplicate_email_without_creating_user(self):
        response = self.client.post(
            REGISTER_URL,
            {"email": self.user.email, "password": "secret-password"},
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(get_user_model().objects.count(), 1)

    def test_registered_uppercase_domain_is_accepted_for_login(self):
        payload = {
            "email": "NewMember@EXAMPLE.COM",
            "password": "secret-password",
        }
        registration = self.client.post(REGISTER_URL, payload)

        self.assertEqual(registration.status_code, status.HTTP_201_CREATED)
        login = self.client.post(LOGIN_URL, payload)

        self.assertEqual(login.status_code, status.HTTP_200_OK)
        self.assertEqual(registration.data["email"], "NewMember@example.com")

    def test_registration_rejects_duplicate_normalized_domain(self):
        payload = {
            "email": "duplicate@example.com",
            "password": "secret-password",
        }
        registration = self.client.post(REGISTER_URL, payload)
        self.assertEqual(registration.status_code, status.HTTP_201_CREATED)

        payload["email"] = "duplicate@EXAMPLE.COM"
        duplicate = self.client.post(REGISTER_URL, payload)

        self.assertEqual(duplicate.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(get_user_model().objects.count(), 2)

    def test_registered_password_whitespace_is_preserved_for_login(self):
        payload = {
            "email": "new@example.com",
            "password": "  secret-password  ",
        }
        registration = self.client.post(REGISTER_URL, payload)

        self.assertEqual(registration.status_code, status.HTTP_201_CREATED)
        login = self.client.post(LOGIN_URL, payload)

        self.assertEqual(login.status_code, status.HTTP_200_OK)
        user = get_user_model().objects.get(email=payload["email"])
        self.assertTrue(user.check_password(payload["password"]))

    def test_registration_requires_valid_email_and_password(self):
        invalid_payloads = (
            {"password": "secret-password"},
            {"email": "", "password": "secret-password"},
            {"email": "invalid-email", "password": "secret-password"},
            {"email": "new@example.com", "password": "1234"},
        )

        for payload in invalid_payloads:
            with self.subTest(payload=payload):
                response = self.client.post(REGISTER_URL, payload)

                self.assertEqual(
                    response.status_code, status.HTTP_400_BAD_REQUEST
                )
                self.assertEqual(get_user_model().objects.count(), 1)

    def test_email_login_token_authenticates_profile_via_header(self):
        response = self.client.post(
            LOGIN_URL,
            {"email": self.user.email, "password": "secret-password"},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {response.data['token']}"
        )
        profile = self.client.get(PROFILE_URL)

        self.assertEqual(profile.status_code, status.HTTP_200_OK)
        self.assertEqual(profile.data["id"], self.user.pk)
        self.assertEqual(profile.data["email"], self.user.email)
        self.assertNotIn("password", profile.data)

    def test_login_preserves_password_whitespace(self):
        password = "  secret-password  "
        self.user.set_password(password)
        self.user.save()

        response = self.client.post(
            LOGIN_URL, {"email": self.user.email, "password": password}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.data)

    def test_login_accepts_uppercase_domain_of_normalized_email(self):
        response = self.client.post(
            LOGIN_URL,
            {"email": "member@EXAMPLE.COM", "password": "secret-password"},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            Token.objects.get(key=response.data["token"]).user, self.user
        )

    def test_inactive_user_cannot_obtain_token(self):
        self.user.is_active = False
        self.user.save()

        response = self.client.post(
            LOGIN_URL,
            {"email": self.user.email, "password": "secret-password"},
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn("token", response.data)
        self.assertFalse(Token.objects.filter(user=self.user).exists())

    def test_invalid_credentials_do_not_create_token(self):
        response = self.client.post(
            LOGIN_URL, {"email": self.user.email, "password": "wrong"}
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn("token", response.data)
        self.assertFalse(Token.objects.filter(user=self.user).exists())

    def test_email_auth_serializer_returns_authenticated_user(self):
        serializer_class = getattr(
            user_serializers, "AuthTokenSerializer", None
        )
        self.assertIsNotNone(serializer_class)
        request = APIRequestFactory().post(LOGIN_URL)
        serializer = serializer_class(
            data={
                "email": self.user.email,
                "password": "secret-password",
            },
            context={"request": request},
        )

        self.assertTrue(serializer.is_valid(), serializer.errors)
        self.assertEqual(serializer.validated_data["user"], self.user)

    def test_profile_update_cannot_escalate_privileges(self):
        token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

        response = self.client.patch(
            PROFILE_URL, {"is_staff": True, "is_superuser": True}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertFalse(self.user.is_staff)
        self.assertFalse(self.user.is_superuser)

    def test_profile_password_update_hashes_password_for_email_login(self):
        token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
        response = self.client.patch(
            PROFILE_URL,
            {"email": "updated@example.com", "password": "updated-secret"},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("updated-secret"))
        self.assertFalse(self.user.check_password("secret-password"))
        self.client.credentials()
        login = self.client.post(
            LOGIN_URL,
            {"email": "updated@example.com", "password": "updated-secret"},
        )
        self.assertEqual(login.status_code, status.HTTP_200_OK)

    def test_updated_password_whitespace_is_preserved_for_login(self):
        password = "  updated-secret  "
        token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
        update = self.client.patch(PROFILE_URL, {"password": password})

        self.assertEqual(update.status_code, status.HTTP_200_OK)
        self.client.credentials()
        login = self.client.post(
            LOGIN_URL, {"email": self.user.email, "password": password}
        )

        self.assertEqual(login.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password(password))

    def test_updated_email_accepts_both_domain_spellings_for_login(self):
        email = "UpdatedMember@EXAMPLE.COM"
        token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
        update = self.client.patch(PROFILE_URL, {"email": email})

        self.assertEqual(update.status_code, status.HTTP_200_OK)
        self.client.credentials()

        for login_email in (email, "UpdatedMember@example.com"):
            with self.subTest(email=login_email):
                login = self.client.post(
                    LOGIN_URL,
                    {"email": login_email, "password": "secret-password"},
                )

                self.assertEqual(login.status_code, status.HTTP_200_OK)

        self.user.refresh_from_db()
        self.assertEqual(self.user.email, "UpdatedMember@example.com")
        self.assertEqual(update.data["email"], self.user.email)


class EmailUserAdminTests(TestCase):
    def setUp(self):
        self.admin_user = get_user_model()(
            email="admin@example.com", is_staff=True, is_superuser=True
        )
        self.admin_user.set_password("Admin-Secret-2026!")
        self.admin_user.save()
        self.client.force_login(self.admin_user)

    def test_admin_user_list_renders_email_without_username_column(self):
        response = self.client.get(reverse("admin:user_user_changelist"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, self.admin_user.email)
        self.assertNotContains(response, "column-username")

    def test_admin_add_form_renders_email_without_username(self):
        response = self.client.get(reverse("admin:user_user_add"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        fields = response.context["adminform"].form.fields
        self.assertIn("email", fields)
        self.assertNotIn("username", fields)

    def test_admin_change_form_renders_email_without_username(self):
        response = self.client.get(
            reverse("admin:user_user_change", args=[self.admin_user.pk])
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        fields = response.context["adminform"].form.fields
        self.assertIn("email", fields)
        self.assertNotIn("username", fields)

    def test_admin_add_form_saves_email_user_with_hashed_password(self):
        response = self.client.post(
            reverse("admin:user_user_add"),
            {
                "email": "new-admin-user@example.com",
                "password1": "Admin-Secret-2026!",
                "password2": "Admin-Secret-2026!",
                "_save": "Save",
            },
        )

        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        user = get_user_model().objects.get(email="new-admin-user@example.com")
        self.assertTrue(user.check_password("Admin-Secret-2026!"))

    def test_admin_change_form_saves_email_user(self):
        response = self.client.post(
            reverse("admin:user_user_change", args=[self.admin_user.pk]),
            {
                "email": "updated-admin@example.com",
                "first_name": "Updated",
                "last_name": "Admin",
                "is_active": "on",
                "is_staff": "on",
                "is_superuser": "on",
                "date_joined_0": self.admin_user.date_joined.strftime(
                    "%Y-%m-%d"
                ),
                "date_joined_1": self.admin_user.date_joined.strftime(
                    "%H:%M:%S"
                ),
                "_save": "Save",
            },
        )

        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.admin_user.refresh_from_db()
        self.assertEqual(self.admin_user.email, "updated-admin@example.com")
        self.assertEqual(self.admin_user.first_name, "Updated")
        self.assertTrue(self.admin_user.check_password("Admin-Secret-2026!"))
