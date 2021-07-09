from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status

from core.models import Survivor


class SurvivorViewsTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.sample_survivor = Survivor.objects.create(
            name="Zé",
            age=18,
            sex="Homem",
            latitude=-6.2839894,
            longitude=-42.4984872,
        )

    def test_create_survivor_missing_params(self):
        payload = dict(
            name="",
            age="",
            sex="",
            latitude="",
            longitude="",
        )

        response = self.client.post("/api/survivors/", payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_survivor_invalid_params(self):
        payload = dict(
            name=0,
            age="invalid",
            sex="invalid",
            latitude="invalid",
            longitude="invalid",
        )

        response = self.client.post("/api/survivors/", payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_survivor_without_inventory(self):
        payload = dict(
            name="Zé",
            age=18,
            sex="Homem",
            latitude=-5.2839894,
            longitude=-44.4984872,
            inventory="",
        )

        response = self.client.post("/api/survivors/", payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_survivor(self):
        payload = dict(
            name="Zé",
            age=18,
            sex="Homem",
            latitude=-5.2839894,
            longitude=-44.4984872,
            inventory=dict(water=4, food=6, medicine=2, ammunition=10),
        )

        response = self.client.post("/api/survivors/", payload, format="json")

        survivor = response.data
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(survivor["name"], "Zé")
        self.assertEqual(survivor["age"], 18)
        self.assertEqual(survivor["sex"], "Homem")
        self.assertEqual(survivor["latitude"], -5.2839894)
        self.assertEqual(survivor["longitude"], -44.4984872)
        self.assertTrue(survivor["inventory"])
