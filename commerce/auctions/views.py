from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listing, Watchitem


def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.all()
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
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


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
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


def create_listing(request):
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        category = request.POST["category"]
        price = request.POST["price"]
        image = request.POST["image"] 
        try:
            current_listing = Listing.objects.create(
                title = title,
                description = description,
                category = category,
                price = price,
                image = image,
            )
            current_listing.save()
        except IntegrityError:
            return render(request, "auctions/create_listing.html", {
                "message": "Test"
            })
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/create_listing.html")
    

def categories(request):
    categories = Listing.objects.values("category")
    return render(request, "auctions/categories.html", {
        "categories": categories
    })
 
    
def category_items(request, name):
    categories = Listing.objects.values("category")
    category_items = Listing.objects.filter(category=name)
    return render(request, "auctions/category_items.html", { 
        "categories": categories,
        "current_category": name,
        "category_items": category_items
    })
    

def listing(request, name):
    try:
        user = User.objects.get(id=request.user.id)
        listing = Listing.objects.get(id=name)
        watchlist = Watchitem.objects.filter(listing=listing, user=user)
        print(len(user.watchlist.all()))
    except Listing.DoesNotExist:
        raise Http404("Listing not found.")
    return render(request, "auctions/listing.html", {
        "listing": listing,
        "watchlist": watchlist
    })
    
    
def update_watchlist(request, name):
    listing = Listing.objects.get(id=name)
    user = User.objects.get(id=request.user.id)
    print(request.method)
    if request.method == "POST":
        watchlist = Watchitem.objects.create(listing=listing, user=user)    
    elif request.method == "GET":
        watchlist = Watchitem.objects.filter(listing=listing, user=user).delete()
    return HttpResponseRedirect(reverse("listing", args=(name,)))
  
    
def watchlist(request, name):
    try:
        watchlist = Watchitem.objects.all(listing=name)
    except Watchitem.DoesNotExist:
        raise Http404("Watchlist not found.")
    return render(request, "auctions/listing.html", {
        "watchlist": watchlist
    })
    
    
def watchitems_count(request):
    user = User.objects.get(id=request.user.id)
    watchitems_count = len(user.watchlist.all())
    return JsonResponse({
        "watchitems_count": watchitems_count
    })