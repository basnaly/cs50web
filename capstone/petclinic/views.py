from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse, HttpResponseServerError
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.forms.models import model_to_dict
from django.views.decorators.csrf import csrf_exempt

import datetime

from .models import User, Pet, Insurance, Visit

PET_ICONS = ['🦮', '🐕‍🦺', '🐶', '🐩', '🐈', '🐈‍⬛', '😼', '😾', '🐇', '🐰', '🐹', '🐁', '🐭', '🦜', '🐦‍⬛', '🦤']
PET_TYPES = ['Dog', 'Cat', 'Rabbit', 'Hamster', 'Bird']
MONTHLY_PRICE = {'Dog': 30, 'Cat': 25, 'Rabbit': 20, 'Hamster': 15, 'Bird': 10}
TYPE_VISIT = ['Illness', 'Vaccination', 'Consulting']
TIME_SLOT = ["9:00", "9:30", "10:00", "10:30", "11:00", "11:30", "16:00", "16:30", "17:00", "17:30", "18:00", "18:30"]

# Create your views here.

def index(request):
    user = User.objects.get(id=request.user.id)
    user_pets = Pet.objects.filter(owner=user)
    if request.method == "GET":
        tomorrow = datetime.datetime.now() + datetime.timedelta(days=1)
        return render(request, "petclinic/index.html", {
            "type_visit_options": TYPE_VISIT,
            "tomorrow": tomorrow,
            "pets": user_pets,
            "time_visits": TIME_SLOT
        })


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
    user_pets = Pet.objects.filter(owner=user)
    if request.method == "POST":
        icon = request.POST["icon"]
        nickname = request.POST["nickname"]
        birth_date = request.POST["birth_date"]
        pet_type = request.POST["pet_type"]
        details = request.POST["details"]
        
        # Attempt to add new pet
        try:
            pet = Pet.objects.create(
                icon = icon,
                nickname = nickname,
                birth_date = birth_date,
                pet_type = pet_type,
                details = details,
                owner = user
            )
            pet.save()
        except IntegrityError:
            return render(request, "petclinic/add_pet.html", {
                "icons": PET_ICONS,
                "types": PET_TYPES,
                "today": datetime.datetime.now()
            })
        return render(request, "petclinic/add_pet.html", {
            "message": f"{nickname} was added!",
            "icons": PET_ICONS,
            "types": PET_TYPES,
            "pets": user_pets,
            "today": datetime.datetime.now()
        })
    else:
        return render(request, "petclinic/add_pet.html", {
            "icons": PET_ICONS,
            "types": PET_TYPES,
            "pets": user_pets,
            "today": datetime.datetime.now()
        })
           

@login_required
def profile(request):
    user = User.objects.get(id=request.user.id)
    user_pets = Pet.objects.filter(owner=user)
    if request.method == "POST":
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        phone_number = request.POST["phone_number"]
        email = request.POST["email"]
       
        # Attempt to update the user
        try:
            user.first_name = first_name
            user.last_name = last_name 
            user.phone_number = phone_number
            user.email = email
            user.save()
        except IntegrityError:
            return render(request, "petclinic/profile.html", {
                "message": "Something went wrong. Try again later.",
                "pets": user_pets,
            })
        return render(request, "petclinic/profile.html", {
                "message": "Your profile was updated!",
                "pets": user_pets,
                "user": user,
            })
            
    else:
        return render(request, "petclinic/profile.html", {
            "pets": user_pets
        })
            
@login_required
def pet_list(request):
    owner = User.objects.get(id=request.user.id)
    user_pets = Pet.objects.filter(owner=owner).values()
    
    # Convert ValuesQuerySet into Python list
    pets_list = [pet for pet in user_pets]
    
    return JsonResponse({
        "pets": pets_list
    })

        
@login_required
def pet_profile(request, name):
    owner = User.objects.get(id=request.user.id)
    user_pets = Pet.objects.filter(owner=owner)
    try:
        pet = Pet.objects.get(id=name)
    except Pet.DoesNotExist:
        raise Http404("It is not your pet!")
    if pet.owner.identical_number != owner.identical_number:
        raise Http404("It is not your pet!")
         
    if request.method == "POST":
        icon = request.POST["icon"]
        nickname = request.POST["nickname"]
        birth_date = request.POST["birth_date"]
        details = request.POST["details"]
        # Attempt to update the pet
        try:
            pet.icon = icon
            pet.nickname = nickname 
            pet.birth_date = birth_date
            pet.details = details
            pet.save()
        except IntegrityError:
            return render(request, "petclinic/pet_profile.html", {
                "message": "Something went wrong. Try again later.",
                "pet": pet,
                "pets": user_pets,
                "today": datetime.datetime.now()
            })
        return render(request, "petclinic/pet_profile.html", {
                "message": f"{nickname} was updated!",
                "pet": pet,
                "pets": user_pets,
                "today": datetime.datetime.now()
            })
            
    else:
        return render(request, "petclinic/pet_profile.html", {
            "pet": pet,
            "pets": user_pets,
            "icons": PET_ICONS,
            "today": datetime.datetime.now()
        })
        
@csrf_exempt        
@login_required
def delete_pet(request, name):
    owner = User.objects.get(id=request.user.id)
    user_pets = Pet.objects.filter(owner=owner)
    try:
        pet = Pet.objects.get(id=name)
    except Pet.DoesNotExist:
        raise Http404("It is not your pet!")
    if pet.owner.identical_number != owner.identical_number:
        raise Http404("It is not your pet!")
    
    if request.method == "DELETE":
        try: 
            pet.delete()
        except IntegrityError:
            return JsonResponse({
                "message": "Something went wrong. Try again later."
            })
        return JsonResponse({
            "message": f"{pet.nickname} was deleted!",
        })
        
        
@login_required
def insurance(request):
    owner = User.objects.get(id=request.user.id)
    user_pets = Pet.objects.filter(owner=owner).values()
    pets_list = [pet for pet in user_pets]
    return render(request, "petclinic/insurance.html", {
            "pets": pets_list,
        })
    
    
@login_required
def pet_insurance(request, name):
    owner = User.objects.get(id=request.user.id)
    try: 
        pet = Pet.objects.get(id=name)
    except Pet.DoesNotExist:
        raise Http404("It is not your pet!")
    if pet.owner.identical_number != owner.identical_number:
        raise Http404("It is not your pet!")
    
    if request.method == "GET":
        insurance = None
        try:
            insurance = Insurance.objects.get(pet=pet)
        except Insurance.DoesNotExist:
            pass
        return render(request, "petclinic/pet_insurance.html", {
                    "pet": pet,
                    "insurance": insurance,  
                    "monthly_price": MONTHLY_PRICE[pet.pet_type],
                    "today": datetime.datetime.now()
                })
    else:
        start_date = request.POST["start_date"]
        monthly_price = MONTHLY_PRICE[pet.pet_type]
        # Attempt to create new insurance
        try:
            insurances = Insurance.objects.filter(pet=pet)
            if len(insurances) == 0:
                insurance = Insurance.objects.create(
                    start_date = start_date,
                    monthly_price = monthly_price,
                    owner = owner,
                    pet = pet
                )
                insurance.save()
            else:
                return render(request, "petclinic/pet_insurance.html", {
                    "pet": pet,
                    "insurance": insurances[0],  
                    "monthly_price": MONTHLY_PRICE[pet.pet_type],
                    "today": datetime.datetime.now()
                })
        except IntegrityError:
            return render(request, "petclinic/pet_insurance.html", {
                "message": "Something went wrong. Try again later.",
                "pet": pet,
                "insurance": insurance,  
                "monthly_price": MONTHLY_PRICE[pet.pet_type],
                "today": datetime.datetime.now()
            })
        return render(request, "petclinic/pet_insurance.html", {
            "message": "We've got your request. We'll call back you during 1 work day.",
            "pet": pet,
            "insurance": insurance,  
            "monthly_price": MONTHLY_PRICE[pet.pet_type],
            "today": datetime.datetime.now()
        })
        

@login_required
def get_times_for_visit(request): 
    # GET /get_times_for_visit?date=abc&type=other&pet=2
    # POST /get_times_for_visit + body {"type": "other", ...}
    
    pass
    
  
@login_required
def save_visit(request): 
    
    pass
        
    
