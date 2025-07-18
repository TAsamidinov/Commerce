from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new_listing", views.new_listing, name="new_listing"),
    path("<int:listing_id>", views.listing, name="listing"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("like/<int:listing_id>", views.like, name="like"),
    path("bid/<int:listing_id>", views.bid, name="bid"),
    path("close/<int:listing_id>", views.close_listing, name="close_listing"),
    path("comment/<int:listing_id>", views.comment, name="comment"),
    path("categories", views.categories, name="categories"),
    path("category/<str:category_name>", views.category_listings, name="category_listings"),
]
