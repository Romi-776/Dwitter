from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Model class for USER related details"""

    # it will contain basic user details like
    # username, password, email, etc.
    pass


class Profile(models.Model):
    # user who's profile is this
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="user_profile"
    )

    profile_pic = models.ImageField(default="default.jpg", upload_to="profile_pics")

    background_img = models.ImageField(
        default="Default_background.jpg", upload_to="bg_img"
    )

    def __str__(self):
        return f"{self.user.username} Profile"


class post(models.Model):
    """Model class for POST related details"""

    posted_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="post_owner"
    )

    posted_on = models.DateTimeField(auto_now_add=True)

    description = models.TextField(null=False, default="")

    def __str__(self):
        return f"{self.posted_by} --> {self.description}"


class follower_following(models.Model):
    """Model class for follower-following related details"""

    followers = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="my_followers"
    )

    following = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="my_following"
    )

    def __str__(self):
        return f"{self.followers} is followed by {self.following}"


class likes(models.Model):
    """Model class for likes related details"""

    # post which is liked
    on_which_post = models.ForeignKey(
        post, on_delete=models.CASCADE, related_name="likes_on_this_post"
    )

    when = models.DateTimeField(auto_now_add=True)

    # user who liked
    who = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="who_liked_this_post"
    )