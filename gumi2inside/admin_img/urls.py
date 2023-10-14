from django.urls import path
from . import views

app_name = "admin_img"
urlpatterns = [
    path("", views.index, name="index"),
    path("update_carousel/<int:number>", views.update_carousel, name="update_carousel"),
    path("static_img/", views.static_img, name="static_img"),
]