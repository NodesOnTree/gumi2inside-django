from django.db import models

# Create your models here.
class Lunch(models.Model):
    date = models.DateField()
    menuCourseType = models.CharField(max_length=5)
    main_menu = models.CharField(max_length=50)
    sub_menu = models.CharField(max_length=50)
    kcal = models.IntegerField()
    carbs = models.IntegerField()
    sodium = models.IntegerField()
    fat = models.IntegerField()
    protein = models.IntegerField()
    image_url = models.URLField(max_length=200)
