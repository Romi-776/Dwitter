from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(post)
admin.site.register(User)
admin.site.register(follower_following)
admin.site.register(likes)