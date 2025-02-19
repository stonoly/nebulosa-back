from django.db import models

class Place(models.Model):
    name = models.CharField(
        max_length=250
    )
    description = models.TextField(
        blank=True,
        null=True
    )
    address = models.ForeignKey(
        'PlaceAdress',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.name
    

class PlaceAdress(models.Model):
    street = models.CharField(
        max_length=250
    )
    number = models.CharField(
        max_length=10
    )
    city = models.CharField(
        max_length=250
    )
    state = models.CharField(
        max_length=250
    )
    country = models.CharField(
        max_length=250
    )
    zip_code = models.CharField(
        max_length=10
    )
    latitude = models.FloatField()
    longitude = models.FloatField()
    