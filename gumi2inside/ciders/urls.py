from django.urls import path
from . import views

app_name = "ciders"
urlpatterns = [
    path("", views.ciders_home , name="main"),
    path("create/", views.ciders_create, name="create"),
    path("create/complete/", views.create_bubble, name="complete"),
    path("<int:bubble_id>/like/", views.like_bubble, name="like_bubble"),
    path("<int:bubble_id>/dislike/", views.dislike_bubble, name="dislike_bubble"),
]