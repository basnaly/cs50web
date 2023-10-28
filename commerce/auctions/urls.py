from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    
    path("create_listing", views.create_listing, name="create_listing"),
    path("categories", views.categories, name="categories"),
    path("categories/<str:name>", views.category_items, name="category_items"),
    path("listing/<str:name>", views.listing, name="listing"),
    
    path("update_watchlist/<str:name>", views.update_watchlist, name="update_watchlist"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("watchitems_count", views.watchitems_count, name="watchitems_count"),
    
    path("bid/<str:name>", views.bid, name="bid"),
    
    path("comments/<str:name>", views.comments, name="comments"),
]
