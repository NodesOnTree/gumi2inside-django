from django.db import models

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

class Comment(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    origin_rboard = models.ForeignKey('Rboard', on_delete=models.CASCADE)
