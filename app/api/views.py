from django.db.models import Avg
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound, ValidationError

from api import serializers
from core.models import Survivor, Inventory


def get_instance(pk) -> Survivor:
    instance = Survivor.objects.filter(pk=pk).first()
    if not instance:
        raise NotFound({"message": [f"Survivor {pk} not found"]})

    if instance.infected_report == 3:
        raise ValidationError({"message": [f"Survivor {pk} is infected"]})

    return instance


class CreateSurvivorView(APIView):
    def post(self, request):
        serializer = serializers.CreateSurvivorSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class RetrieveSurvivorView(APIView):
    def get(self, request, pk):
        instance = get_instance(pk)
        serializer = serializers.SurvivorSerializer(instance=instance)

        return Response(serializer.data, status=status.HTTP_200_OK)


class UpdateSurvivorLocationView(APIView):
    def post(self, request, pk):
        instance = get_instance(pk)

        serializer = serializers.UpdateSurvivorLocationSerializer(
            instance=instance, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


class UpdateSurvivorInfectedView(APIView):
    def post(self, request, pk):
        instance = get_instance(pk)

        total_report = instance.infected_report
        total_report += 1
        Survivor.objects.filter(id=pk).update(infected_report=total_report)
        instance.refresh_from_db()

        serializer = serializers.SurvivorSerializer(instance=instance)

        return Response(serializer.data, status=status.HTTP_200_OK)


class ExchangeView(APIView):
    def post(self, request):
        serializer = serializers.ExchangeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        survivor_1 = get_instance(serializer.data["survivor_1"])
        survivor_2 = get_instance(serializer.data["survivor_2"])

        items_survivor_1 = serializer.data["items_survivor_1"]
        items_survivor_2 = serializer.data["items_survivor_2"]

        survivor_1_points = survivor_1.calculate_points(items_survivor_1)
        survivor_2_points = survivor_2.calculate_points(items_survivor_2)

        if not survivor_2_points >= survivor_1_points:
            raise ValidationError(
                {
                    "message": [
                        f"Survivor {survivor_2.id} has not enough points to exchange"
                    ]
                }
            )

        survivor_1_inventory_update = survivor_1.inventory.swap(
            items_survivor_1, items_survivor_2
        )
        survivor_2_inventory_update = survivor_2.inventory.swap(
            items_survivor_2, items_survivor_1
        )

        Inventory.objects.filter(survivor=survivor_1).update(
            **survivor_1_inventory_update
        )
        Inventory.objects.filter(survivor=survivor_2).update(
            **survivor_2_inventory_update
        )

        return Response(status=status.HTTP_200_OK)


class ReportsView(APIView):
    def get(self, request):
        total_survivors = Survivor.objects.count()
        total_infected_survivors = Survivor.objects.filter(infected_report=3).count()
        total_uninfected_survivors = total_survivors - total_infected_survivors

        average_resource = dict(
            water=int(
                Inventory.objects.filter(survivor__infected_report=0)
                .aggregate(Avg("water"))
                .get("water__avg", 0)
            ),
            food=int(
                Inventory.objects.filter(survivor__infected_report=0)
                .aggregate(Avg("food"))
                .get("food__avg", 0)
            ),
            medicine=int(
                Inventory.objects.filter(survivor__infected_report=0)
                .aggregate(Avg("medicine"))
                .get("medicine__avg", 0)
            ),
            ammunition=int(
                Inventory.objects.filter(survivor__infected_report=0)
                .aggregate(Avg("ammunition"))
                .get("ammunition__avg", 0)
            ),
        )

        survivors_infected = Survivor.objects.filter(infected_report=3).all()
        points_lost = 0
        for survivor in survivors_infected:
            points_lost += survivor.inventory.total_points()

        data = dict(
            infected_survivors=int(total_infected_survivors / total_survivors * 100),
            uninfected_survivors=int(
                total_uninfected_survivors / total_survivors * 100
            ),
            average_resource=average_resource,
            points_lost=points_lost,
        )

        serializer = serializers.ReportsSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
