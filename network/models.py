from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Model class for USER related details"""

    pass


class post(models.Model):
    """Model class for POST related details"""

    posted_by = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="post_owner"
    )
    posted_on = models.DateTimeField(auto_now_add=True)
    description = models.TextField(null=False, default="")

    def __str__(self):
        return f"{self.posted_by} --> {self.description}"


class follower_following(models.Model):
    followers = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="my_followers"
    )
    following = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="my_following"
    )

    def __str__(self):
        return f"{self.followers} is followed by {self.following}"