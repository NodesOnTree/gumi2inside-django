from django.urls import path
from . import views

app_name = 'articles'
urlpatterns = [
    path('home/', views.home, name='home'),
    path('create/', views.create, name="create"),
    path('watch_articles/', views.watch_articles, name='watch_articles'),
    path('list/', views.list, name="list"),
]   
