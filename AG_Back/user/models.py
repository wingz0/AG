from django.contrib.auth.models import AbstractUser
from django.db import models

#Check
class CustomUser(AbstractUser): 
    
    groups = models.ManyToManyField(
        blank=True,
        related_name="custom_user_groups", 
        related_query_name="custom_user",
    )
    user_permissions = models.ManyToManyField(
        blank=True,
        related_name="custom_user_permissions",
        related_query_name="custom_user",
    )

    def __str__(self):
        return self.username
