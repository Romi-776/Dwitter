from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile", views.profile, name="profile"),
    path("share_post", views.share_post, name="share_post"),
    path("<int:user_id>", views.others_profile, name="others_profile"),
    path("follow_unfollow", views.follow_unfollow, name="follow_unfollow"),
    path("like_post", views.like_post, name="like_post"),
    path("posts_of_following", views.posts_of_following, name="posts_of_following"),
    # API Routes
    path("update_post", views.update_post, name="update_post"),
    path("update_profile", views.update_profile, name="update_profile"),
    path("update_profile_pic", views.update_profile_pic, name="update_profile_pic"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)