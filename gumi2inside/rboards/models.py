from django.db import models
from django.conf import settings


# Create your models here.
class Rboard(models.Model):
    title = models.CharField(max_length=30)
    content = models.TextField()
    textsize = models.TextField()
    red = models.TextField()
    green = models.TextField()
    blue = models.TextField()
    image = models.ImageField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    visited_count = models.IntegerField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    like_count = models.IntegerField(default=0)
    dislike_count = models.IntegerField(default=0)
    liked_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="real_liked_articles")
    disliked_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="real_disliked_articles")


class Comment(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    origin_rboard = models.ForeignKey('Rboard', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    like_count = models.IntegerField(default=0)
    dislike_count = models.IntegerField(default=0)
    comment_liked_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="real_liked_comments")
    comment_disliked_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="real_disliked_comments")
