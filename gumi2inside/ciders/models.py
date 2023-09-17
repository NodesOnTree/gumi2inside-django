from django.db import models

# Create your models here.
class Bubble(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    expired_at = models.DateTimeField()
    like_count = models.IntegerField()
    dislike_count = models.IntegerField()
