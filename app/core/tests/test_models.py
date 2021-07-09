from django.test import TestCase

from ..models import Survivor, Inventory


class ModelsTests(TestCase):
    def test_create_survivor(self):
        survivor = Survivor.objects.create(
            name="Zé", age=18, sex="Homem", latitude=-5.2839894, longitude=-44.4984872
        )

        self.assertEqual(survivor.name, "Zé")
        self.assertEqual(survivor.age, 18)
        self.assertEqual(survivor.sex, "Homem")
        self.assertEqual(survivor.latitude, -5.2839894)
        self.assertEqual(survivor.longitude, -44.4984872)
        self.assertEqual(survivor.infected_report, 0)

    def test_update_survivor(self):
        survivor = Survivor.objects.create(
            name="Zé", age=18, sex="Homem", latitude=-5.2839894, longitude=-44.4984872
        )

        Survivor.objects.filter(id=survivor.id).update(
            age=19, infected_report=3, latitude=-5.0872465, longitude=-42.8058265
        )

        survivor.refresh_from_db()
        self.assertEqual(survivor.age, 19)
        self.assertEqual(survivor.latitude, -5.0872465)
        self.assertEqual(survivor.longitude, -42.8058265)
        self.assertEqual(survivor.infected_report, 3)

    def test_retrieve_survivor(self):
        Survivor.objects.create(
            name="Zé", age=18, sex="Homem", latitude=-5.2839894, longitude=-44.4984872
        )

        survivor = Survivor.objects.first()
        self.assertEqual(survivor.name, "Zé")
        self.assertEqual(survivor.age, 18)

    def test_create_inventory(self):
        survivor = Survivor.objects.create(
            name="Zé", age=18, sex="Homem", latitude=-5.2839894, longitude=-44.4984872
        )
        inventory = Inventory.objects.create(
            water=4, food=6, medicine=2, ammunition=10, survivor=survivor
        )

        self.assertEqual(inventory.water, 4)
        self.assertEqual(inventory.food, 6)
        self.assertEqual(inventory.medicine, 2)
        self.assertEqual(inventory.ammunition, 10)
        self.assertEqual(inventory.survivor, survivor)

    def test_update_inventory(self):
        survivor = Survivor.objects.create(
            name="Zé", age=18, sex="Homem", latitude=-5.2839894, longitude=-44.4984872
        )
        inventory = Inventory.objects.create(
            water=4, food=6, medicine=2, ammunition=10, survivor=survivor
        )

        Inventory.objects.filter(survivor=survivor).update(
            water=5, food=7, medicine=3, ammunition=11
        )

        inventory.refresh_from_db()
        self.assertEqual(inventory.water, 5)
        self.assertEqual(inventory.food, 7)
        self.assertEqual(inventory.medicine, 3)
        self.assertEqual(inventory.ammunition, 11)

    def test_retrieve_inventory(self):
        survivor = Survivor.objects.create(
            name="Zé", age=18, sex="Homem", latitude=-5.2839894, longitude=-44.4984872
        )
        Inventory.objects.create(
            water=4, food=6, medicine=2, ammunition=10, survivor=survivor
        )

        inventory = Inventory.objects.first()
        self.assertEqual(inventory.survivor, survivor)
        self.assertEqual(inventory.food, 6)
