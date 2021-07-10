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

    def test_update_survivor_location_with_invalid_id(self):
        payload = dict(
            latitude=-5.2839894,
            longitude=-44.4984872,
        )

        response = self.client.post(
            "/api/survivors/99/location/", payload, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_survivor_location_invalid_params(self):
        payload = dict(
            latitude="invalid",
            longitude="invalid",
        )

        response = self.client.post(
            f"/api/survivors/{self.sample_survivor.id}/location/",
            payload,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_survivor_location(self):
        payload = dict(
            latitude=-5.2839894,
            longitude=-44.4984872,
        )

        response = self.client.post(
            f"/api/survivors/{self.sample_survivor.id}/location/",
            payload,
            format="json",
        )

        survivor = response.data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(survivor["latitude"], -5.2839894)
        self.assertEqual(survivor["longitude"], -44.4984872)

    def test_update_survivor_infected_report_with_invalid_id(self):
        response = self.client.post("/api/survivors/99/infected/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_survivor_infected(self):
        response = self.client.post(
            f"/api/survivors/{self.sample_survivor.id}/infected/"
        )

        self.sample_survivor.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.sample_survivor.infected_report, 1)

    def test_update_survivor_already_infected(self):
        Survivor.objects.filter(id=self.sample_survivor.id).update(infected_report=3)
        self.sample_survivor.refresh_from_db()

        payload = dict(
            latitude=-5.2839894,
            longitude=-44.4984872,
        )

        response_1 = self.client.post(
            f"/api/survivors/{self.sample_survivor.id}/location/",
            payload,
            format="json",
        )
        response_2 = self.client.post(
            f"/api/survivors/{self.sample_survivor.id}/infected/"
        )

        self.assertEqual(response_1.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_2.status_code, status.HTTP_400_BAD_REQUEST)
