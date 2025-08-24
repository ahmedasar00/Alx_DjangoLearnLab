from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class CustomerUserModel(AbstractUser):
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField("profile_picture/", blank=True, null=True)
    followers = models.ManyToManyField(
        "self", symmetrical=False, related_name="following", blank=True
    )
    followering = models.ManyToManyField(
        "self", symmetrical=False, related_name="followers", blank=True
    )

    def __str__(self):
        return self.username
