from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile", views.profile, name="profile"),
    path("share_post", views.share_post, name="share_post"),
    path("<int:user_id>", views.others_profile, name="others_profile"),
    path("change_follower_following", views.change_follower_following, name="change_follower_following"),
]
