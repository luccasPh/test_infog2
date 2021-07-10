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


class CreateSurvivorSerializer(SurvivorSerializer):
    class Meta(SurvivorSerializer.Meta):
        ...

    def create(self, validated_data):
        inventory_data = validated_data.pop("inventory")
        survivor = models.Survivor.objects.create(**validated_data)
        inventory_data["survivor"] = survivor
        models.Inventory.objects.create(**inventory_data)

        return survivor


class UpdateSurvivorLocationSerializer(SurvivorSerializer):
    class Meta(SurvivorSerializer.Meta):
        read_only_fields = ("name", "sex", "age", "infected_report")


class SurvivorsItemsSerializer(serializers.Serializer):
    water = serializers.IntegerField(required=False)
    food = serializers.IntegerField(required=False)
    medicine = serializers.IntegerField(required=False)
    ammunition = serializers.IntegerField(required=False)


class ExchangeSerializer(serializers.Serializer):
    survivor_1 = serializers.IntegerField()
    survivor_2 = serializers.IntegerField()
    items_survivor_1 = SurvivorsItemsSerializer()
    items_survivor_2 = SurvivorsItemsSerializer()


class ReportsSerializer(serializers.Serializer):
    infected_survivors = serializers.IntegerField()
    uninfected_survivors = serializers.IntegerField()
    average_resource = SurvivorsItemsSerializer()
    points_lost = serializers.IntegerField()
