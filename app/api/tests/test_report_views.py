from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from core.models import Survivor, Inventory


class ReportsViewsTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.survivor_1 = Survivor.objects.create(
            name="Survivor 1",
            age=22,
            sex="Homem",
            latitude=-5.2839894,
            longitude=-44.4984872,
        )
        self.survivor_2 = Survivor.objects.create(
            name="Survivor 2",
            age=22,
            sex="Mulher",
            latitude=-5.2839894,
            longitude=-44.4984872,
        )
        self.survivor_3 = Survivor.objects.create(
            name="Survivor 3",
            age=22,
            sex="Homem",
            latitude=-5.2839894,
            longitude=-44.4984872,
            infected_report=3,
        )
        Inventory.objects.bulk_create(
            [
                Inventory(
                    water=4, food=6, medicine=2, ammunition=10, survivor=self.survivor_1
                ),
                Inventory(
                    water=7, food=3, medicine=4, ammunition=2, survivor=self.survivor_2
                ),
                Inventory(
                    water=3, food=3, medicine=4, ammunition=5, survivor=self.survivor_3
                ),
            ]
        )

    def test_percentage_infected_survivors(self):
        response = self.client.get("/api/reports/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["infected_survivors"], 33)

    def test_percentage_uninfected_survivors(self):
        response = self.client.get("/api/reports/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["uninfected_survivors"], 66)

    def test_average_resource_per_survivor(self):
        response = self.client.get("/api/reports/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["average_resource"],
            {"water": 5, "food": 4, "medicine": 3, "ammunition": 6},
        )

    def test_points_lost_infected_survivor(self):
        response = self.client.get("/api/reports/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["points_lost"], 34)
