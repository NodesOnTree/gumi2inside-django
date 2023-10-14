from django.db import models

# Create your models here.
class Article(models.Model):
    title = models.CharField(max_length=30)
    content = models.TextField()
    textsize = models.TextField()
    red = models.TextField()
    green = models.TextField()
    blue = models.TextField()
    image = models.ImageField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    visited_count = models.IntegerField()
    like_count = models.IntegerField(default=0)
    dislike_count = models.IntegerField(default=0)

class Comment(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    origin_article = models.ForeignKey('Article', on_delete=models.CASCADE)
    like_count = models.IntegerField(default=0)
    dislike_count = models.IntegerField(default=0)