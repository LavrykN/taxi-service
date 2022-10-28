from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Driver

DRIVER_URL = reverse("taxi:driver-list")


class PublicDriverTests(TestCase):
    def test_login_required(self):
        res = self.client.get(DRIVER_URL)

        self.assertNotEqual(res.status_code, 200)


class PrivateDriverTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="password123"
        )
        self.client.force_login(self.user)

    def test_retrieve_driver(self):
        get_user_model().objects.create_user(
            username="Anton123",
            password="qwe123",
            first_name="Anton",
            last_name="Sisun",
            license_number="ABC12345"
        )

        response = self.client.get(DRIVER_URL)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["driver_list"]),
            list(Driver.objects.all())
        )
        self.assertTemplateUsed(response, "taxi/driver_list.html")

    def test_search_driver(self):
        get_user_model().objects.create_user(
            username="joyce.byers",
            password="qwe123",
            first_name="Joyce",
            last_name="Byers",
            license_number="JOY26458"
        )
        get_user_model().objects.create_user(
            username="mike.wheeler",
            password="qwe123",
            first_name="Mike",
            last_name="Wheeler",
            license_number="MIK25131"
        )

        response = self.client.get(DRIVER_URL + "?username=joy")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["driver_list"]), 1)
        self.assertEqual(
            Driver(**response.context["driver_list"].values()[0]).username,
            "joyce.byers"
        )
