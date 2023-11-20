from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse, HttpResponseServerError
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import User, Pet

# Create your views here.

def index(request):
    return render(request, "petclinic/index.html")


def login_view(request):
    if request.method == "POST":
        
        # Attempt to sign user in
        identical_number = request.POST["identical_number"]
        password = request.POST["password"]
        user = authenticate(request, username=identical_number, password=password)
        
        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "petclinic/login.html", {
                "message": "Invalid identical number or password!"
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
            user = User.objects.create_user(
                username = identical_number, 
                first_name = first_name, 
                last_name = last_name, 
                phone_number = phone_number, 
                email = email, 
                password = password
            )
            user.save()
        except IntegrityError:
            return render(request, "petclinic/register.html", {
                "message": "User already taken!"
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    
    else:
        return render(request, "petclinic/register.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


@login_required
def add_pet(request):
    user = User.objects.get(id=request.user.id)
    if request.method == "POST":
        icon = request.POST["icon"]
        nickname = request.POST["nickname"]
        birth_date = request.POST["birth_date"]
        pet_type = request.POST["pet_type"]
        details = request.POST["details"]
        owner = user
        
        # Attempt to add new pet
        try:
            pet = Pet.objects.create(
                icon = icon,
                nickname = nickname,
                birth_date = birth_date,
                pet_type = pet_type,
                details = details,
                owner = owner
            )
            pet.save()
        except IntegrityError:
            return render(request, "petclinic/add_pet.html")
        return render(request, "petclinic/add_pet.html", {
            "message": f"{nickname} was added!"
        })
    else:
        return render(request, "petclinic/add_pet.html")
        

@login_required
def profile(request, name):
    pass
