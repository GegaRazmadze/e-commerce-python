from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("watch_list/", views.watch_list, name="watch_list"),
    path("add/", views.add, name="create_add"),
    path("<int:item_id>/listing_page", views.listing_page, name="listing_page"),
    path("<int:item_id>/turn_off", views.turn_off, name="turn_off"),
    path("my_items/", views.my_items, name="my_items"),
    path("category/", views.category, name="category"),
]
