from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import *


def index(request):
    """Home page of the website"""

    # getting all the posts that are posted by all the user
    # sorted according to recently posted
    all_posts = post.objects.order_by("posted_on").reverse()

    posts_and_likes = []
    for p in all_posts:
        posts_and_likes.append((p, likes.objects.filter(on_which_post=p).count()))
    
    return render(
        request,
        "network/index.html",
        {
            "all_posts": posts_and_likes,
        },
    )


def login_view(request):
    """Login page of the website"""

    # when the login form is submitted
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
    """Loging out of the website"""

    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    """Registration page of the website"""

    # when the user submitted the form
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
    """Seeing the personal profile of the login user"""

    # getting all the posts of that user
    posts = post.objects.filter(posted_by=request.user)

    # getting the no. of followers and following
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
    """Sharing the post to everyone"""

    # checking that the user is logged in and the request is valid
    if request.method == "POST" and request.user.is_authenticated:

        # getting the post details, checking it and saving it in the DB
        post_des = request.POST["description"]

        if post_des == "":
            return HttpResponse("Empty post, Can't share this!")

        new_post = post(posted_by=request.user, description=post_des)
        new_post.save()

        return HttpResponseRedirect(reverse("index"))

    # user is not logged in or the request isn't valid
    else:
        return render(
            request, "network/login.html", {"message": "Login to share your Post!"}
        )


def others_profile(request, user_id):
    """Checking the profile of other people"""

    # getting the user whose profile the currently logged in user wants to check
    user = User.objects.get(pk=user_id)

    # it will store the text which will be inserted in the follow_unfollow_button
    follow_unfollow = ""

    # will store that the button should be viewed as black or red
    style = ""

    # getting all the instances from the follower_following model
    all_follower_following = follower_following.objects.all()

    # some random flag for later use
    flag = 0

    # traversing through all the instances
    for i in all_follower_following:
        # checking that the currently logged in user follows the currently viewing profile
        if str(i.followers) == str(user.username) and str(i.following) == str(
            request.user.username
        ):

            # then the button should contain the unfollow text
            follow_unfollow = "unfollow"
            style = "danger"
            flag = 1
            break

    # otherwise the text should be follow
    if not flag:
        follow_unfollow = "follow"
        style = "dark"

    # checking that the user exists or not
    if user:
        # getting the user's details
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
                "follow_button_text": follow_unfollow,
                "follow_button_style": style,
            },
        )
    return HttpResponse("NO user with that name!!!")


def follow_unfollow(request):
    """when someone clicks on the follow button"""

    if request.method == "POST":

        text_returned = request.POST["follow_unfollow_button"]
        print(text_returned)

        if text_returned == "follow":
            # who clicked the button and on whom's profile
            follow_request_from = request.user.username
            follow_request_to = ""

            try:
                follow_request_to = request.POST["username"]
            except IntegrityError:
                return HttpResponse(
                    "Something went wrong while fetching the name of the person to whom you sent a follow request"
                )

            # getting those users details from the DB
            new_follower = User.objects.get(username=follow_request_to)
            new_following = User.objects.get(username=follow_request_from)

            # trying to create that entry of follow request to someone in the DB
            try:
                new_follower_following = follower_following.objects.create(
                    following=new_following, followers=new_follower
                )
                new_follower_following.save()
            except IntegrityError:
                return HttpResponse(
                    "Something went wrong while creating a new follower_following instance"
                )
            # returning to that user's id on whom's profile the follow button is clicked
            return HttpResponseRedirect(
                reverse("others_profile", args=[new_follower.id])
            )
        else:
            """when someone clicks on the unfollow button"""

            # who clicked the button and on whom's profile
            unfollow_request_from = request.user.username
            unfollow_request_to = ""

            try:
                unfollow_request_to = request.POST["username"]
            except IntegrityError:
                return HttpResponse(
                    "Something went wrong while fetching the name of the person to whom you sent an unfollow request"
                )

            # getting those users details from the DB
            person_who_unfollows = User.objects.get(username=unfollow_request_from)
            person_who_get_unfollowed = User.objects.get(username=unfollow_request_to)

            # trying to delete that entry from the DB
            try:
                un_follower_following = follower_following.objects.get(
                    following=person_who_unfollows, followers=person_who_get_unfollowed
                )
                un_follower_following.delete()
            except IntegrityError:
                return HttpResponse(
                    "Something went wrong while deleting the un_follower_following instance"
                )

            # returning to that user's id on whom's profile the follow button is clicked
            return HttpResponseRedirect(
                reverse("others_profile", args=[person_who_get_unfollowed.id])
            )

def like_post(request):
    if request.user.is_authenticated:
        print(f"{request.GET['this_post']}")
        return HttpResponse("You just liked a post")
    else:
        return render(
                request,
                "network/login.html",
                {"message": "You should Login first!"},
            )