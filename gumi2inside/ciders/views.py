from datetime import timedelta
from django.utils import timezone
from django.shortcuts import redirect, render
from .models import Bubble

# Create your views here.

def ciders_home(request):
    bubbles = view_bubbles()
    context = {
        'bubbles': bubbles
    }
    return render(request, "ciders/main.html", context)

def ciders_create(request):
    return render(request, "ciders/create.html")

def create_bubble(request):
    bubble = Bubble()
    bubble.content = request.POST.get('content')
    bubble.like_count = 0
    bubble.dislike_count = 0
    bubble.expired_at = timezone.now() + timedelta(hours=1)
    bubble.save()

    return redirect("/ciders")

def like_bubble(request, bubble_id):
    bubble = Bubble.objects.get(id = bubble_id)
    bubble.like_count += 1
    bubble.expired_at += timedelta(minutes=10)
    bubble.save()

    return redirect

def dislike_bubble(request, bubble_id):
    bubble = Bubble.objects.get(id = bubble_id)
    bubble.dislike_count -= 1  
    bubble.expired_at -= timedelta(minutes=10)  
    bubble.save()

    return redirect

def view_bubbles():
    
    expired_bubbles = Bubble.objects.filter(expired_at__lte=timezone.now())
    expired_bubbles.delete()

    return Bubble.objects.all()