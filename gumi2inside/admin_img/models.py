from django.db import models

class Carousel(models.Model):
    number = models.IntegerField()
    img_url = models.URLField()
    status = models.TextField(default="Carousel")

class Static_img(models.Model):
    name = models.TextField()
    img_url = models.URLField()
    status = models.TextField(default="Static")

