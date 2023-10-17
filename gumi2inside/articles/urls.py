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
    path("comment_like/<int:comment_pk>/", views.like_comment, name="like_comment"),
    path("comment_dislike/<int:comment_pk>/", views.dislike_comment, name="dislike_comment"),
    path('polls_list/', views.polls_list, name='polls_list'),
    path('polls_list/user/', views.polls_list_by_user, name='polls_list_by_user'),
    path('polls_add/', views.polls_add, name='polls_add'),
    path('polls_edit/<int:poll_id>/', views.polls_edit, name='polls_edit'),
    path('polls_delete/<int:poll_id>/', views.polls_delete, name='polls_delete'),
    path('polls_end/<int:poll_id>/', views.polls_endpoll, name='polls_end_poll'),
    path('polls_edit/<int:poll_id>/choice/add/', views.polls_add_choice, name='polls_add_choice'),
    path('polls_edit/choice/<int:choice_id>/', views.polls_choice_edit, name='polls_choice_edit'),
    path('polls_delete/choice/<int:choice_id>/',
         views.polls_choice_delete, name='choice_delete'),
    path('polls_<int:poll_id>/', views.poll_detail, name='polls_detail'),
    path('polls_<int:poll_id>/vote/', views.poll_vote, name='polls_vote'),
]
