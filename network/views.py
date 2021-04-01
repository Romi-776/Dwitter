from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import *


def index(request):
    all_posts = post.objects.order_by("posted_on").reverse()

    return render(
        request,
        "network/index.html",
        {
            "all_posts": all_posts,
        },
    )


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(
                request,
                "network/login.html",
                {"message": "Invalid username and/or password."},
            )
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]

        # Ensure that all the fields are not empty
        if username == "":
            return render(
                request, "network/register.html", {"message": "Enter your Username!"}
            )
        elif email == "":
            return render(
                request, "network/register.html", {"message": "Enter your Email ID!"}
            )
        elif password == "":
            return render(
                request, "network/register.html", {"message": "Enter your Password!"}
            )
        elif confirmation == "":
            return render(
                request,
                "network/register.html",
                {"message": "Enter Password Confirmation!"},
            )

        # Ensure that password and confirmation match
        if password != confirmation:
            return render(
                request, "network/register.html", {"message": "Passwords must match!"}
            )

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(
                request, "network/register.html", {"message": "Username already taken."}
            )
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


def profile(request):
    posts = post.objects.filter (posted_by=request.user)

    followers = User.objects.get(username=request.user.username).my_followers.count()
    following = User.objects.get(username=request.user.username).my_following.count()

    return render(
        request,
        "network/profile.html",
        {
            "username": request.user.username,
            "email": request.user.email,
            "posts": posts,
            "followers": followers,
            "following": following,
        },
    )


def share_post(request):
    if request.method == "POST" and request.user.is_authenticated:
        post_des = request.POST["description"]

        if post_des == "":
            return HttpResponse("Empty post, Can't share this!")

        new_post = post(posted_by=request.user, description=post_des)
        new_post.save()

        return HttpResponseRedirect(reverse("index"))
    else:
        return render(
            request, "network/login.html", {"message": "Login to share your Post!"}
        )


def others_profile(request, user_id):
    user = User.objects.get(pk=user_id)
    if user:
        posts = post.objects.filter(posted_by=user)
        followers = User.objects.get(username=user.username).my_followers.count()
        following = User.objects.get(username=user.username).my_following.count()

        return render(
            request,
            "network/profile.html",
            {
                "username": user.username,
                "email": user.email,
                "posts": posts,
                "followers": followers,
                "following": following,
            },
        )
    return HttpResponse("NO user with that name!!!")
