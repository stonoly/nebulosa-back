from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(
        'auth.User',
        on_delete=models.CASCADE,
        primary_key=True
    )
    birth_date = models.DateField(
        null=True, 
        blank=True
    )
