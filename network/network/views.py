from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.urls import reverse
from django import forms

from .models import User, Posts, Follow
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

class PostForm(forms.Form):
    new_post = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Post', 'class': 'form-control', 'rows': 3}), label='')
    
 
def index(request):
    posts = Posts.objects.all().order_by("-created")
    paginator = Paginator(posts, 10)
    page_num = request.GET.get('page', 1)
    try:
        page_obj = paginator.page(int(page_num))
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    return render(request, "network/index.html", {
        "posts": page_obj.object_list,
        "title": "All posts",
        "has_next": page_obj.has_next(),
        "has_previous":page_obj.has_previous(),
        "next_page": int(page_num) + 1,
        "previous_page": int(page_num) - 1,
        "path": "index" 
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


@login_required
def new_post(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            new_post = form.cleaned_data["new_post"]
            user = User.objects.get(id=request.user.id)
        try:
            current_post = Posts.objects.create(
                body = new_post,
                owner = user,
            )
            current_post.save()
        except IntegrityError:
            return render(request, "network/new_post.html", {
                "message": "Test"
            })
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/new_post.html", {
            "form": PostForm
        })
  
        
def profile(request, name):
    try: 
        user_profile = User.objects.get(id=name) # bob
        user_posts = user_profile.posts.order_by("-created") # bob's posts
        followers_count = len(user_profile.followers.all())
        folowings_count = len(user_profile.followings.all())
        if request.user.is_authenticated:
            loggedin_user = User.objects.get(id=request.user.id)
            is_follow = len(user_profile.followers.filter(follower=loggedin_user))
        else:
            is_follow = False
    except User.DoesNotExist:
        raise Http404("Profile not found.")
    return render(request, "network/profile.html", {
        "user_profile": user_profile,
        "user_posts": user_posts,
        "followers_count": followers_count,
        "folowings_count": folowings_count,
        "is_follow": is_follow
    })
    
    
@login_required
def follow(request, name):
    if request.method == "POST":
        follower = User.objects.get(id=request.user.id) # charly
        following = User.objects.get(id=name) # bob
        try:
            follow = Follow.objects.create(
                follower = follower,
                following = following
            )
            follow.save()            
        except Follow.DoesNotExist:
            raise Http404("Follow not found.") 
    return HttpResponseRedirect(reverse("profile", args=(name,))) 


@login_required
def unfollow(request, name):
    if request.method == "POST":
        follower = User.objects.get(id=request.user.id)
        following = User.objects.get(id=name)
        try:
            unfollow = Follow.objects.filter(follower=follower, following=following).delete()
        except Follow.DoesNotExist:
            raise Http404("Follow not found.") 
    return HttpResponseRedirect(reverse("profile", args=(name,)))     
            
       
@login_required
def following(request):    
    current_user = User.objects.get(id=request.user.id)
    page_num = request.GET.get('page', 1)
    try:
        current_user_followings = Follow.objects.filter(follower=current_user).values_list("following") # max->charly, max->bob
        list_posts_followings = Posts.objects.filter(owner__in=current_user_followings).order_by("-created")
        paginator = Paginator(list_posts_followings, 10)
        page_obj = paginator.page(int(page_num))
    except Follow.DoesNotExist:
        raise Http404("Follow not found.") 
    except Posts.DoesNotExist:
        raise Http404("Posts not found.") 
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    return render (request, "network/index.html", {
        "posts": page_obj.object_list,
        "title": current_user.username.title() + '`s followings',
        "has_next": page_obj.has_next(),
        "has_previous":page_obj.has_previous(),
        "next_page": int(page_num) + 1,
        "previous_page": int(page_num) -1, 
        "path": "following"     
    })
    
                   