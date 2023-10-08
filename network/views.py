from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.core.paginator import Paginator
from django.shortcuts import render
from django.urls import reverse
import json
from django.views.decorators.csrf import csrf_exempt

from .models import User, Post, Like, Follow

def index(request):
    posts = Post.objects.all().order_by("-date")

    paginator = Paginator(posts, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    # find posts that current user like (id post)
    if request.user.is_authenticated:
        liked_posts = Like.objects.filter(username=request.user).values_list("post", flat=True)
    else:
        liked_posts = []

    return render(request, "network/index.html", {
        "posts": posts,
        "page_obj": page_obj,
        "liked_posts": liked_posts,
    })
    
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
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
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
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
    
def following(request):
    following_user = Follow.objects.filter(follower=request.user)   # get users that current user are following
    posts = Post.objects.none()
    for user in following_user:
        user = user.user_being_followed
        post = Post.objects.filter(username=user)
        posts = posts.union(post)

    posts = posts.order_by("-date")

    paginator = Paginator(posts, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "network/index.html", {
        "posts": posts,
        "page_obj": page_obj,
        "following": True
    })

def follow(request, user_id):
    user = User.objects.get(pk=user_id)
    if request.method == "POST":
        new_follow = Follow(
            follower = request.user,
            user_being_followed = user 
        )
        new_follow.save()
        return HttpResponseRedirect(reverse("profile", args=[user_id]))

    return profile(request, user_id)

def unfollow(request, user_id):
    user = User.objects.get(pk=user_id)
    if request.method == "POST":
        unfollow = Follow.objects.get(follower=request.user, user_being_followed=user)
        unfollow.delete()
        return HttpResponseRedirect(reverse("profile", args=[user_id]))

    return profile(request, user_id)

def profile(request, user_id):
    user = User.objects.get(pk=user_id)
    num_followers = Follow.objects.filter(user_being_followed=user).count()    
    num_following = Follow.objects.filter(follower=user).count()
    following = Follow.objects.filter(follower=request.user)   # get those follows which the curent user is following
    posts = Post.objects.filter(username=user).order_by("-date")

    followable = False
    if not following.filter(user_being_followed=user).exists():    # check if the profile's user exist in those follows
        followable = True

    paginator = Paginator(posts, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    # find posts that current user like (id post)
    if request.user.is_authenticated:
        liked_posts = Like.objects.filter(username=request.user).values_list("post", flat=True)
    else:
        liked_posts = []

    return render(request, "network/profile.html", {
        "user": user,
        "num_followers": num_followers,
        "num_following": num_following,
        "following": following,
        "posts": posts,
        "followable": followable,
        "page_obj": page_obj,
        "liked_posts": liked_posts,
    })

def new_post(request):
    if request.method == "POST":
        post = request.POST["post"]
        if post:
            new_post = Post(
                username = request.user,
                content = post,
            )
            new_post.save()
        return HttpResponseRedirect(reverse("index"))

    return index(request)

@csrf_exempt
def edit(request, post_id):
    if request.method == "POST":
        data = json.loads(request.body)
        content = data.get("content", "")

        post = Post.objects.get(pk=post_id)
        post.content = content
        post.save()
        return JsonResponse({"message": "Edit post successfully", "content": content})

def is_like(request, post_id):
    # find posts that current user like (id post)
    liked_posts = Like.objects.filter(username=request.user).values_list("post", flat=True)
    liked_posts = list(liked_posts)

    return JsonResponse({"liked_posts": liked_posts})
 
@csrf_exempt
def toggle_like(request, post_id):
    if request.method == "POST":
        data = json.loads(request.body)
        like_count = int(data.get("like_count", 0))
        is_like = bool(data.get("is_like", False))

        if not is_like:
            like_count += 1

            post = Post.objects.get(pk=post_id)
            post.like = like_count
            post.save()

            # create a new Like object
            new_like = Like(
                username = request.user,
                post = post
            )
            new_like.save()
            return JsonResponse({"message": "Like succesfully", "like_count": post.like})
        else:
            like_count -= 1

            post = Post.objects.get(pk=post_id)
            post.like = like_count
            post.save()

            # delete Like object
            old_like = Like.objects.get(username=request.user, post=post)
            old_like.delete()
            return JsonResponse({"message": "Unlike succesfully", "like_count": post.like})
