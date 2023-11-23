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
    
]