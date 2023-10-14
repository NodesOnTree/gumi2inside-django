from django.urls import path
from . import views

app_name = "articles"
urlpatterns = [
    path("create/", views.create, name="create"),
    path("new/", views.new, name="new"),
    path("complete/", views.complete, name="complete"),
    path("delete/<int:pk>/", views.delete, name="delete"),
    path("detail/<int:pk>/", views.detail, name="detail"),
    path("articles_list/", views.articles_list, name="articles_list"),
    path("comment/<int:pk>/", views.comment, name="comment"),
    path("like/<int:article_pk>/", views.like_article, name="like_article"),
    path("dislike/<int:article_pk>/", views.dislike_article, name="dislike_article"),
    path("like/<int:comment_pk>/", views.like_comment, name="like_comment"),
    path("dislike/<int:comment_pk>/", views.dislike_comment, name="dislike_comment"),
]
