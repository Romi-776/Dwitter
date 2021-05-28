from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
import json
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.core.paginator import Paginator

from .models import *


def index(request):
    """Home page of the website"""

    # getting all the posts that are posted by all the user
    # sorted according to recently posted
    all_posts = post.objects.order_by("posted_on").reverse()

    posts_liked_by_this_user = []
    if request.user.is_authenticated:
        posts_liked_by_this_user = [
            post.on_which_post.id for post in likes.objects.filter(who=request.user)
        ]
    posts_and_likes = []
    # attatching posts and likes on each post into single list
    for p in all_posts:
        posts_and_likes.append((p, likes.objects.filter(on_which_post=p).count()))

    # getting posts that need to be shown on a single page.
    """Currently showing only 1 post per page but needs to be changed to 10"""
    paginator = Paginator(posts_and_likes, 10)
    page_number = request.GET.get("page", 1)
    page = paginator.get_page(page_number)

    # getting info that the current page have next or previous page or not
    if page.has_next():
        next_url = f"?page={page.next_page_number()}"
    else:
        next_url = ""

    if page.has_previous():
        prev_url = f"?page={page.previous_page_number()}"
    else:
        prev_url = ""

    return render(
        request,
        "network/index.html",
        {
            "page": page,
            "on_index_page": True,
            "next_page_url": next_url,
            "prev_page_url": prev_url,
            "my_liked_posts": posts_liked_by_this_user,
        },
    )


def posts_of_following(request):
    """Following page to see the following people's posts only """

    # getting all the following people's ids
    my_following = follower_following.objects.filter(following=request.user)

    # checking that there's at least one person that i'm following
    if not len(my_following):
        return render(
            request,
            "network/index.html",
            {
                "on_index_page": False,
            },
        )

    # storing the names of the people that i'm following
    my_following_names = []
    for i in my_following:
        my_following_names.append(User.objects.get(username=i.followers))
    # getting the likes count on that posts
    posts_and_likes = []

    for user in my_following_names:
        this_users_post = post.objects.filter(posted_by=user)
        for each_post in this_users_post:
            posts_and_likes.append(
                (each_post, likes.objects.filter(on_which_post=each_post).count())
            )

    # getting posts that need to be shown on a single page.
    """Currently showing only 1 post per page but needs to be changed to 10"""
    paginator = Paginator(posts_and_likes, 1)
    page_number = request.GET.get("page", 1)
    page = paginator.get_page(page_number)

    # getting info that the current page have next or previous page or not
    if page.has_next():
        next_url = f"?page={page.next_page_number()}"
    else:
        next_url = ""

    if page.has_previous():
        prev_url = f"?page={page.previous_page_number()}"
    else:
        prev_url = ""

    return render(
        request,
        "network/index.html",
        {
            "page": page,
            "on_index_page": False,
            "next_page_url": next_url,
            "prev_page_url": prev_url,
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
        message = ""

        return render(request, "network/login.html", {"message": message})


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

        # Attempt to create new user and its corresponding profile
        try:
            user = User.objects.create_user(username, email, password)
            user.save()

            new_user_profile = Profile.objects.create(user=user)
            new_user_profile.save()
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

    user = User.objects.get(username=request.user.username)

    return render(
        request,
        "network/profile.html",
        {
            "user": user,
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
                "user": user,
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


@login_required
@csrf_exempt
def like_post(request):
    """Like Unlike the post """

    # checking that the user is authenticated and the request is from genuine place
    if request.method == "POST":

        # getting the data that needs to be updated
        data = json.loads(request.body)

        # getting the id of the post on which the user want to like the post
        post_id = data.get("post_id")
        this_post = post.objects.get(pk=post_id)

        # if the post is already liked then we're un liking the post otherwise
        # we're liking the post
        try:
            likes.objects.get(on_which_post=this_post, who=request.user.id).delete()
        except ObjectDoesNotExist:
            try:
                new_like = likes.objects.create(
                    on_which_post=this_post, who=request.user
                )
                new_like.save()
            except IntegrityError:
                return JsonResponse(
                    {
                        "error": "Something went wrong while creating a new like instance"
                    },
                    status=400,
                )

        # returning to the index page
        return JsonResponse({"Message": "Like count Updated!"}, status=201)
    else:
        return JsonResponse({"error": "POST request required"}, status=400)


@csrf_exempt
@login_required
def update_post(request):
    # checking that the request is sent via post
    if request.method != "POST":
        return JsonResponse({"error": "POST request required"}, status=400)

    # getting the data that needs to be updated
    data = json.loads(request.body)

    # getting the post that needs to be updated
    updated_post = post.objects.filter(pk=int(data.get("post_id"))).update(
        description=data.get("updated_description")
    )

    # post is updated, just confirming
    return JsonResponse({"Message": "Post Updated!"}, status=201)


@csrf_exempt
@login_required
def update_profile(request):
    # checking that the request is sent via post
    if request.method != "POST":
        return JsonResponse({"error": "POST request required"}, status=400)

    # getting the data that needs to be updated
    data = json.loads(request.body)

    # getting the user whose profile  needs to be updated
    user = User.objects.get(username=data.get("user"))

    # getting that user's profile
    profile_to_update = Profile.objects.filter(user=user)

    # updating the profile
    profile_to_update.update(
        profile_pic=data.get("profile_pic"), background_img=data.get("bg_img")
    )

    # if the user changed his username
    changed_name = data.get("name")

    # change the name of that user
    if changed_name != user.username:
        user.update(username=changed_name)

    # Profile is updated, just confirming
    return JsonResponse({"Message": "Profile Updated!"}, status=201)


@login_required
def update_profile_pic(request):
    if request.method == "POST":

        return HttpResponseRedirect(reverse("profile"))