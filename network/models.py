from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class post(models.Model):
    posted_by = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="post_owner"
    )
    posted_on = models.DateTimeField(auto_now_add=True)
    description = models.TextField(null=False, default="")

    def __str__(self):
        return f"{self.posted_by} --> {self.description}"
