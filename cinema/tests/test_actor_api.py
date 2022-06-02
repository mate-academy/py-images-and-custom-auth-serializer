from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from cinema.models import Actor
from cinema.serializers import ActorSerializer
from user.tests.test_user_api import create_user

ACTOR_URL = reverse("cinema:actor-list")


def sample_actor(**params):
    defaults = {
        "first_name": "test_name",
        "last_name": "test_last",
    }
    defaults.update(params)

    return Actor.objects.create(**defaults)


class PublicActorApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(ACTOR_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateActorApiTests(TestCase):
    def setUp(self):
        self.user = create_user(
            username="test_admin",
            email="test@test.com",
            password="testpass",
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_get_actors(self):
        sample_actor()

        response = self.client.get(ACTOR_URL)

        actors = Actor.objects.all()
        serializer = ActorSerializer(actors, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_post_actors(self):
        payload = {
            "first_name": "test_name",
            "last_name": "test_last",
        }

        response = self.client.post(ACTOR_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class AdminActorApiTests(TestCase):
    def setUp(self):
        self.user = create_user(
            username="test_admin",
            email="test@test.com",
            password="testpass",
            is_staff=True,
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_post_actors(self):
        payload = {
            "first_name": "test_name",
            "last_name": "test_last",
        }

        response = self.client.post(ACTOR_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_retrieve_actor(self):
        sample_actor()

        response = self.client.get(f"{ACTOR_URL}1/")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_put_actor(self):
        sample_actor()

        response = self.client.put(f"{ACTOR_URL}1/", {})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_actor(self):
        sample_actor()

        response = self.client.delete(f"{ACTOR_URL}1/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
