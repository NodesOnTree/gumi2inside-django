from django.shortcuts import render
from .models import Carousel,Static_img
from img_upload import img_upload
# Create your views here.

def index(request):
    return render(request, "admin_img/index.html")


def update_carousel(request, number):
    try:
        carousel = Carousel.objects.get(number=number)
        carousel.delete()
        carousel = Carousel.objects.create(number=number, img_url="Not")
        img_upload(request, carousel)
    except:
        carousel = Carousel.objects.create(number=number, img_url="Not")
        img_upload(request, carousel)
                    
    return render(request, "admin_img/index.html")


def static_img(request):
    name = request.POST.get('name')
    try:
        static_img = Static_img.objects.get(name=name)
        static_img.delete()
        static_img = Static_img.objects.create(name=name, img_url="Not")
        img_upload(request, static_img)
    except:
        static_img = Static_img.objects.create(name=name, img_url="Not")
        img_upload(request, static_img)
                    
    return render(request, "admin_img/index.html")
