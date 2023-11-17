from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse, HttpResponseServerError
from django.shortcuts import render
from django.urls import reverse
from django import forms
from django.views.decorators.csrf import csrf_exempt
import json
from django.db import models

from .models import User, Posts, Follow, Likes
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


class PostForm(forms.Form):
    new_post = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Post', 'class': 'form-control', 'rows': 3}), label='')
    
 
def index(request):
    if request.user.is_authenticated:
        loggedin_user = User.objects.get(id=request.user.id)
    else:
        loggedin_user = None
    
    # Get posts of all users with likes_count and liked_by_loggedin_user count per post
    posts = Posts.objects.all().order_by("-created").annotate(
        likes_count=models.Count('likes'),
        liked_by_loggedin_user=models.Count('likes', filter=models.Q(likes__owner=loggedin_user))
    )

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
            
            # Get new post from the form and user id from request
            new_post = form.cleaned_data["new_post"]
            user = User.objects.get(id=request.user.id)
            
            if not new_post:
                return render(request, "network/new_post.html", {
                    "message": "Post cannot be empty!",
                    "form": form
                })
                
        # Attempt to save the form in db
        try:
            current_post = Posts.objects.create(
                body = new_post,
                owner = user,
            )
            current_post.save()
        except IntegrityError:
            return render(request, "network/new_post.html", {
                "message": "Something went wrong. Please try again.",
                "form": form
            })
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/new_post.html", {
            "form": PostForm
        })
  
        
def profile(request, name):
    try: 
        # Get user profile page
        user_profile = User.objects.get(id=name) 
        
        if request.user.is_authenticated:
            loggedin_user = User.objects.get(id=request.user.id)
            is_follow = len(user_profile.followers.filter(follower=loggedin_user)) 
            
        else:
            loggedin_user = None
            is_follow = False
        
        # Get user's posts with likes_count and liked_by_loggedin_user count
        user_posts = user_profile.posts.order_by("-created").annotate(  
            likes_count=models.Count('likes'),
            liked_by_loggedin_user=models.Count('likes', filter=models.Q(likes__owner=loggedin_user))
        )   
        followers_count = len(user_profile.followers.all())
        folowings_count = len(user_profile.followings.all())
           
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
        
        # Get follower (loggedin user) and user he wants to follow
        follower = User.objects.get(id=request.user.id)
        following = User.objects.get(id=name)
        
        # Attempt to save follow row in db
        try:
            follow = Follow.objects.create(
                follower = follower,
                following = following
            )
            
            if not follow.is_valid_follow():
                return HttpResponseRedirect(reverse("profile", args=(name,))) 
                
            follow.save()            
        except Follow.DoesNotExist:
            raise Http404("Follow not found.") 
    return HttpResponseRedirect(reverse("profile", args=(name,))) 


@login_required
def unfollow(request, name):
    if request.method == "POST":
        
        # Get follower and followings from db 
        follower = User.objects.get(id=request.user.id)
        following = User.objects.get(id=name)
        
        # Attempt to delete follow row from db
        try:
            unfollow = Follow.objects.filter(follower=follower, following=following).delete()
        except Follow.DoesNotExist:
            raise Http404("Follow not found.") 
    return HttpResponseRedirect(reverse("profile", args=(name,)))     
            
       
@login_required
def following(request):    
    loggedin_user = User.objects.get(id=request.user.id)
    page_num = request.GET.get('page', 1)
    
    # Attempt to get followings of loggedin user and their posts
    try:
        loggedin_user_followings = Follow.objects.filter(follower=loggedin_user).values_list("following") 
        list_posts_followings = Posts.objects.filter(owner__in=loggedin_user_followings).order_by("-created").annotate(
            likes_count=models.Count('likes'),
            liked_by_loggedin_user=models.Count('likes', filter=models.Q(likes__owner=loggedin_user))
        )
        print(list_posts_followings)
        
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
        "title": loggedin_user.username.title() + '`s followings',
        "has_next": page_obj.has_next(),
        "has_previous":page_obj.has_previous(),
        "next_page": int(page_num) + 1,
        "previous_page": int(page_num) -1, 
        "path": "following"     
    })
    

@csrf_exempt   
@login_required
def edit(request, name):
    if request.method == "POST":
        
        # Get loggedin user and selected post from db 
        loggedin_user = User.objects.get(id=request.user.id)
        selected_post = Posts.objects.get(id=name) 
        
        # Validate that the post belongs to loggedin user
        if (loggedin_user == selected_post.owner): 
            corrected_post = json.loads(request.body)
            selected_post.body = corrected_post['body']
            
            if not selected_post.is_valid_post():
                return HttpResponse("Post cannot be empty!", status=500) 
            try:
                selected_post.save()
            except: 
                return JsonResponse({
                    "message": "Something went wrong."
                }, status=500) 
            return JsonResponse({
                "message": "Your post was updated!"
            })
        else:
            return JsonResponse({
                "message": "It's not your post!"
            }, status=403)
            

@csrf_exempt  
@login_required
def like(request, name):
    if request.method == "POST":
        
        # Get loggedin user and post to like
        loggedin_user = User.objects.get(id=request.user.id)
        liked_post = Posts.objects.get(id=name)
        
        # Attempt to create new like
        try:
            like = Likes.objects.create(
                owner = loggedin_user,
                post = liked_post
            )
            if not like.is_valid_like():
                return JsonResponse({
                    "message": "You cannot like your own post!"
                }, status=500)
                
            like.save()
            
        except Likes.DoesNotExist:
            raise Http404("Likes not found")
        return JsonResponse({})


@csrf_exempt  
@login_required
def unlike(request, name):
    if request.method == "POST":
        loggedin_user = User.objects.get(id=request.user.id)
        liked_post = Posts.objects.get(id=name)
        
        # Attempt to delete existing like
        try:
            unlike = Likes.objects.filter(owner=loggedin_user, post=liked_post).delete()
        except Likes.DoesNotExist:
            raise Http404("Likes not found")
        return JsonResponse ({})