from django.db import models

class Place(models.Model):
    name = models.CharField(
        max_length=250
    )

    def __str__(self) -> str:
        return self.nom