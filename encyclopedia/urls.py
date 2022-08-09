from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:TITLE>", views.title, name="title"),
    path("search", views.search_title, name="search"),
    path("create", views.create, name="create"),
    path("wiki/<str:TITLE>/edit", views.edit, name="edit"),
    path("random", views.random, name="random")
]
