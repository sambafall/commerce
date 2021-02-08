from django.urls import path
from django.contrib.auth.decorators import login_required

from . import views

app_name="auctions"

urlpatterns = [

    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("add_listing", views.add_listing, name="add_listing"),
    path("<int:listing_id>", views.listing_page, name="listing_page"),
    path("<int:listing_id>/update_watchlist", views.add_to_watchlist, name="addtowatchlist"),
    path("watchlist", views.watchlist_page, name="watchlist"),
    path("<int:listing_id>/update_status", views.close_listing, name="close_listing"),
    path("categories", views.get_categories, name="categories"),
    path("<str:category>", views.get_category_listings, name="get_category_listings"),
]
