from django.db import models

# Create your models here.
class Lunch(models.Model):
    date = models.DateField()
    menuCourseType = models.CharField(max_length=5)
    main_menu = models.CharField(max_length=50)
    sub_menu = models.CharField(max_length=50)
    kcal = models.CharField(max_length=10)
    carbs = models.CharField(max_length=10)
    sodium = models.CharField(max_length=10)
    fat = models.CharField(max_length=10)
    protein = models.CharField(max_length=10)
    image_url = models.URLField(max_length=200)
