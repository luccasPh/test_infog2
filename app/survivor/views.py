from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound, ValidationError

from survivor import serializers
from core.models import Survivor


def get_instance(pk):
    instance = Survivor.objects.filter(pk=pk).first()
    if not instance:
        raise NotFound({"message": ["Survivor not found"]})

    if instance.infected_report == 3:
        raise ValidationError({"message": ["Survivor is infected"]})

    return instance


class CreateSurvivorView(APIView):
    def post(self, request):
        serializer = serializers.CreateSurvivorSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


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
