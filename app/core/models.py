from enum import Enum
from django.db import models
from rest_framework.exceptions import ValidationError


class ItemsPoint(Enum):
    water = 4
    food = 3
    medicine = 2
    ammunition = 1


class Survivor(models.Model):
    name = models.CharField(max_length=255)
    age = models.IntegerField()
    sex = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()
    infected_report = models.IntegerField(default=0)

    def calculate_points(self, items) -> int:
        total = 0
        for key, value in items.items():
            inventory_value = getattr(self.inventory, key)
            if inventory_value <= value or inventory_value == 0:
                raise ValidationError(
                    {"message": [f"Survivor {self.id} has not sufficient {key}"]}
                )
            else:
                total += ItemsPoint[key].value * value

        return total

    def __str__(self):
        return self.name


class Inventory(models.Model):
    water = models.IntegerField(blank=True, null=True)
    food = models.IntegerField(blank=True, null=True)
    medicine = models.IntegerField(blank=True, null=True)
    ammunition = models.IntegerField(blank=True, null=True)

    survivor = models.OneToOneField(Survivor, on_delete=models.CASCADE)

    def swap(self, items_remove, items_receive):
        update_inventory = {}
        for key, value in items_remove.items():
            update_inventory[key] = getattr(self, key) - value

        for key, value in items_receive.items():
            if key in update_inventory:
                update_inventory[key] += value
            else:
                update_inventory[key] = getattr(self, key) + value

        return update_inventory

    def total_points(self) -> int:
        total = 0
        for item in ItemsPoint:
            key = item.name
            if getattr(self, key) > 0:
                total += getattr(self, key) * item.value

        return total

    def __str__(self):
        return f"Inventory of {self.survivor.name}"
