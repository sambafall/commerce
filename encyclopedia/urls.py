from django.urls import path

from . import views

app_name = 'wiki'

urlpatterns = [
    path("", views.index, name="index"),
    path("<str:TITLE>", views.entry_page, name="entry_page"),
    path("results/", views.search, name="search"),
    path("new/", views.add_page, name="new"),
    path("save/", views.create_page, name="create"),
    path("edit/", views.edit_page, name="edit_page"),
    path("random/", views.random_page, name="random_page")
]
