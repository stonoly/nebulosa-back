from django.db import models

class Tag(models.Model):
    name = models.CharField(
        max_length=250
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )
    creator = models.ForeignKey(
        'auth.User',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name

class PlaceTag(models.Model):
    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
        related_name='place_tags'
    )
    place = models.ForeignKey(
        'places.Place',
        on_delete=models.CASCADE,
        related_name='place_tags'
    )
    description = models.TextField(
        blank=True,
        null=True
    )
    grade = models.FloatField(
        default=0
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )
    creator = models.ForeignKey(
        'auth.User',
        on_delete=models.CASCADE
    )

    class Meta:
        unique_together = ('tag', 'place')

    def __str__(self):
        return f"{self.tag.name} - {self.place.name}"