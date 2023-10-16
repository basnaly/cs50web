from django.urls import path

from . import views

urlpatterns = [
    path("wiki", views.index, name="index"),
    path("wiki/search", views.search, name="query"),
    path("wiki/random", views.random_search, name="random"), 
    path("wiki/add", views.add, name="add"),
    path("wiki/<str:name>", views.title, name="title"),     
]
