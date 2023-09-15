from django.urls import path
from . import views

app_name = 'articles'
urlpatterns = [
    path('index/', views.index, name='index'),
<<<<<<< HEAD
    path('watch_articles/', views.watch_articles, name='watch_articles'),
]
=======
    path('create/', views.create, name="create"),
    path('list/', views.list, name="list"),
]   
>>>>>>> b62371fffe115d444bb9b4fbf3d40cd70ffa4490
