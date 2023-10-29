from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listing, Watchitem, Bid, Comments


def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.filter(is_active=True)
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
        user = User.objects.get(id=request.user.id)
        try:
            current_listing = Listing.objects.create(
                title = title,
                description = description,
                category = category,
                price = price,
                image = image,
                owner = user,
            )
            current_listing.save()
            print(current_listing)
        except IntegrityError:
            return render(request, "auctions/create_listing.html", {
                "message": "Test"
            })
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/create_listing.html")
    

def categories(request):
    categories = Listing.objects.values("category").distinct()
    return render(request, "auctions/categories.html", {
        "categories": categories
    })
 
    
def category_items(request, name):
    categories = Listing.objects.values("category").distinct()
    category_items = Listing.objects.filter(category=name, is_active=True)
    return render(request, "auctions/category_items.html", { 
        "categories": categories,
        "current_category": name,
        "category_items": category_items,
    })
    

def listing(request, name):
    try:
        listing = Listing.objects.get(id=name)
        if request.user and request.user.id:
            user = User.objects.get(id=request.user.id)
            watchlist = Watchitem.objects.filter(listing=listing, user=user)
        else:
            watchlist = None
        
        last_bid = None
        bids = list(listing.bids.all())
        bids_count = len(bids)
        if bids_count > 0:
            last_bid = bids[-1]
        comments = list(listing.comments.all())
    except Listing.DoesNotExist:
        raise Http404("Listing not found.")
    return render(request, "auctions/listing.html", {
        "listing": listing,
        "watchlist": watchlist,
        "bids_count": bids_count,
        "last_bid": last_bid,
        "comments": comments,
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
  
    
def watchlist(request):
    try:
        user = User.objects.get(id=request.user.id)
        watchlist = user.watchlist.all() 
    except Watchitem.DoesNotExist:
        raise Http404("Watchlist not found.")
    return render(request, "auctions/watchlist.html", {
        "watchlist": watchlist,
    })
    
    
def watchitems_count(request):
    user = User.objects.get(id=request.user.id)
    watchitems_count = len(user.watchlist.all())
    return JsonResponse({
        "watchitems_count": watchitems_count
    })
    
    
def bid(request, name):
    if request.method == "POST":
        bid = request.POST["bid"] # bid from input
        user = User.objects.get(id=request.user.id) 
        listing = Listing.objects.get(id=name)
        bids = list(listing.bids.all()) # bids from related_name
        if not bids:            
            if int(bid) < listing.price:
                return HttpResponseRedirect(reverse("listing", args=(name, )))
        else:
            last_bid = bids[-1].bid
            if int(bid) <= last_bid:
                return HttpResponseRedirect(reverse("listing", args=(name, )))
        try:
            current_bid = Bid.objects.create(
                bid = bid,
                user = user,
                listing = listing,
            )
            current_bid.save()
        except Bid.DoesNotExist:
            raise Http404("Bid not found.")
        return HttpResponseRedirect(reverse("listing", args=(name,)))
        

def comments(request, name):
    if request.method == "POST":
        comment = request.POST["comment"]
        user = User.objects.get(id=request.user.id)
        listing = Listing.objects.get(id=name)
        comments = list(listing.comments.all())
        try:
            current_comment = Comments.objects.create(
                comment = comment,
                user = user,
                listing = listing
            )
            current_comment.save()
        except Comments.DoesNotExist:
            raise Http404("Comments not found.")
        return HttpResponseRedirect(reverse("listing", args=(name,)))
    
    
def deactivate(request, name):
    if request.method == "POST":
        listing = Listing.objects.get(id=name)
        listing.is_active=False
        listing.save()
        return HttpResponseRedirect(reverse("listing", args=(name,)))
    
    
def activate(request, name):
    if request.method == "POST":
        listing = Listing.objects.get(id=name)
        listing.is_active=True
        listing.save()
        return HttpResponseRedirect(reverse("listing", args=(name,)))
        