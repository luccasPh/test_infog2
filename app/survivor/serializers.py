from rest_framework import serializers

from core import models


class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Inventory
        fields = ("water", "food", "medicine", "ammunition")


class SurvivorSerializer(serializers.ModelSerializer):
    inventory = InventorySerializer()

    class Meta:
        model = models.Survivor
        fields = "__all__"

    def create(self, validated_data):
        inventory_data = validated_data.pop("inventory")
        survivor = models.Survivor.objects.create(**validated_data)
        inventory_data["survivor"] = survivor
        models.Inventory.objects.create(**inventory_data)

        return survivor
