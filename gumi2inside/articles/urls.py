from django.urls import path
from . import views

app_name = "articles"
urlpatterns = [
    path("create/", views.create, name="create"),
    path("new/", views.new, name="new"),
    path("complete/", views.complete, name="complete"),
    path("delete/<int:pk>", views.delete, name="delete"),
    path("detail/<int:pk>", views.detail, name="detail"),
    path("list/", views.list, name="list"),
]
