from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from core import models


class ExchangeViewsTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.survivor_1 = models.Survivor.objects.create(
            name="Survivor 1",
            age=20,
            sex="Mulher",
            latitude=-5.2839894,
            longitude=-44.4984872,
        )
        self.survivor_2 = models.Survivor.objects.create(
            name="Survivor 2",
            age=26,
            sex="Homem",
            latitude=-5.2839894,
            longitude=-44.4984872,
        )

        models.Inventory.objects.bulk_create(
            [
                models.Inventory(
                    water=4, food=6, medicine=2, ammunition=10, survivor=self.survivor_1
                ),
                models.Inventory(
                    water=6, food=3, medicine=7, ammunition=5, survivor=self.survivor_2
                ),
            ]
        )

    def test_exchange_items_with_invalid_params(self):
        payload = dict(
            survivor_1="invalid",
            survivor_2="invalid",
            items_survivor_1=dict(water="invalid", food="invalid"),
            items_survivor_2=dict(
                ammunition="invalid",
            ),
        )

        response = self.client.post("/api/exchange/", payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_exchange_items_with_not_found_survivors(self):
        payload = dict(
            survivor_1=99,
            survivor_2=99,
            items_survivor_1=dict(water=1, food=2),
            items_survivor_2=dict(
                ammunition=7,
            ),
        )

        response = self.client.post("/api/exchange/", payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_exchange_items_with_infected_survivors(self):
        models.Survivor.objects.filter(id=self.survivor_2.id).update(infected_report=3)
        payload = dict(
            survivor_1=self.survivor_1.id,
            survivor_2=self.survivor_2.id,
            items_survivor_1=dict(water=1, food=2),
            items_survivor_2=dict(
                ammunition=7,
            ),
        )

        response = self.client.post("/api/exchange/", payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_exchange_items_with_insufficient_item(self):
        payload = dict(
            survivor_1=self.survivor_1.id,
            survivor_2=self.survivor_2.id,
            items_survivor_1=dict(water=99, food=99),
            items_survivor_2=dict(
                ammunition=99,
            ),
        )

        response = self.client.post("/api/exchange/", payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_exchange_items_with_insufficient_points(self):
        payload = dict(
            survivor_1=self.survivor_1.id,
            survivor_2=self.survivor_2.id,
            items_survivor_1=dict(
                water=2, food=2  # 2 water = 8, 2 = food 6, point = 14
            ),
            items_survivor_2=dict(
                ammunition=1,  # 1 ammunition = 1, point = 1
            ),
        )

        response = self.client.post("/api/exchange/", payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_exchange_items(self):
        payload = dict(
            survivor_1=self.survivor_1.id,
            survivor_2=self.survivor_2.id,
            items_survivor_1=dict(
                food=2, ammunition=4  # 2 food = 9, 4 ammunition = 4, point = 10
            ),
            items_survivor_2=dict(
                water=1,
                food=1,
                medicine=2,  # 1 water = 4, 1 food = 3, 2 medicine = 4, point = 11
            ),
        )

        response = self.client.post("/api/exchange/", payload, format="json")

        self.survivor_1.refresh_from_db()
        self.survivor_2.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertEqual(self.survivor_1.inventory.water, 5)
        self.assertEqual(self.survivor_1.inventory.food, 5)
        self.assertEqual(self.survivor_1.inventory.ammunition, 6)
        self.assertEqual(self.survivor_1.inventory.medicine, 4)

        self.assertEqual(self.survivor_2.inventory.water, 5)
        self.assertEqual(self.survivor_2.inventory.food, 4)
        self.assertEqual(self.survivor_2.inventory.medicine, 5)
        self.assertEqual(self.survivor_2.inventory.ammunition, 9)
