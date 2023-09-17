from django.urls import path
from . import views

app_name = "ciders"
urlpatterns = [
    path("", views.ciders_home , name="main"),
    path("create/", views.create_bubble, name="create"),
    path("<int:bubble_id>/like/", views.like_bubble, name="like_bubble"),
    path("<int:bubble_id>/dislike/", views.dislike_bubble, name="dislike_bubble"),
]