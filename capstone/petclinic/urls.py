from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    
    path("login", views.login_view, name="login"),
    path("register", views.register, name="register"),
    path("logout", views.logout_view, name="logout"),
    path("add_pet", views.add_pet, name="add_pet"),
    
    path("profile", views.profile, name="profile"),
    path("pet_list", views.pet_list, name="pet_list"),
    path("pet_profile/<str:name>", views.pet_profile, name="pet_profile"),
    path("delete_pet/<str:name>", views.delete_pet, name="delete_pet"),
    
    path("insurance", views.insurance, name="insurance"),
    path("pet_insurance/<str:name>", views.pet_insurance, name="pet_insurance"),
    
    path("get_times_for_visit", views.get_times_for_visit, name="get_times_for_visit"),
    path("save_visit", views.save_visit, name="save_visit"),
    
    path("show_vaccinations", views.show_vaccinations, name="show_vaccinations"),
    
    path("notification", views.notification, name="notification"),
    path("cancel_visit/<str:name>", views.cancel_visit, name="cancel_visit"),
]