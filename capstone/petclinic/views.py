from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse, HttpResponseServerError
from django.shortcuts import render
from django.urls import reverse

from .models import User

# Create your views here.

def index(request):
    return render(request, "petclinic/index.html")


def login(request):
    if request.method == "POST":
        
        # Attempt to sign user in
        identical_number = request.POST["identical_number"]
        password = request.POST["password"]
        user = authenticate(request, identical_number=identical_number, password=password)
        
        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "petclinic/login.html", {
                "message": "Invalid identical_number or password"
            })
    else:    
        return render(request, "petclinic/login.html")


def register(request):
    if request.method == "POST":
        identical_number = request.POST["identical_number"]
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        phone_number = request.POST["phone_number"]
        email = request.POST["email"]
        
        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "petclinic/register.html", {
                "message": "Password must match conformation."
            })
            
        # Attempt to create new user
        try:
            new_user = User.objects.create_user(identical_number, first_name, last_name, phone_number, email, password)
            new_user.save()
        except IntegrityError:
            return render(request, "petclinic/register.html", {
                "message": "User already taken"
            })
        login(request, new_user)
        return HttpResponseRedirect(reverse("index"))
    
    else:
        return render(request, "petclinic/register.html")


def logout(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))
