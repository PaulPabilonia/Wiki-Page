from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.entry, name="entry"),
    path("editPage",views.editPage, name='editPage'),
    path("saveEdit",views.saveEdit,name="saveEdit"),
    path("randomPage", views.randomPage,name="randomPage"),
    path("newPage", views.newPage,name="newPage"),
    path("saveNewPage", views.saveNewPage, name="saveNewPage"),
    path("search",views.search,name="search")
]
