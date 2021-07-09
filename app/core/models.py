from django.db import models

# Create your models here.


class Survivor(models.Model):
    name = models.CharField(max_length=255)
    age = models.IntegerField()
    sex = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()
    infected_report = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Inventory(models.Model):
    water = models.IntegerField(blank=True, null=True)
    food = models.IntegerField(blank=True, null=True)
    medicine = models.IntegerField(blank=True, null=True)
    ammunition = models.IntegerField(blank=True, null=True)

    survivor = models.OneToOneField(Survivor, on_delete=models.CASCADE)

    def __str__(self):
        return f"Inventory of {self.survivor.name}"
