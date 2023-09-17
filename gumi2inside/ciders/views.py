from datetime import timedelta
from django.utils import timezone
from django.shortcuts import redirect, render
from .models import Bubble

# Create your views here.

def ciders_home(request):
    width_and_bubbles = view_bubbles()
    context = {
        'bubbles': width_and_bubbles
    }
    return render(request, "ciders/main.html", context)

def create_bubble(request):
    bubble = Bubble()
    bubble.content = request.POST.get('content')
    bubble.like_count = 0
    bubble.dislike_count = 0
    bubble.expired_at = timezone.now() + timedelta(hours=3)
    bubble.save()
    print("버블이 작성됐어요!")

    return redirect("/ciders")

def like_bubble(request, bubble_id):
    bubble = Bubble.objects.get(id = bubble_id)
    bubble.like_count += 1
    bubble.expired_at += timedelta(minutes=10)
    bubble.save()
    print("좋아요!")
    return redirect("/ciders")

def dislike_bubble(request, bubble_id):
    bubble = Bubble.objects.get(id = bubble_id)
    bubble.dislike_count -= 1  
    bubble.expired_at -= timedelta(minutes=10)  
    bubble.save()
    print("싫어요ㅠ")
    return redirect("/ciders")

def bubble_algo(time):
    a = -36000
    b = 180  
    c = 250  
    
    score = a / (time + b) + c
    return score

def view_bubbles():
    
    expired_bubbles = Bubble.objects.filter(expired_at__lte=timezone.now())
    expired_bubbles.delete()

    bubbles = Bubble.objects.all()

    sorted_bubbles = []

    for bubble in bubbles:
        current_time = timezone.now()
        time_dif = bubble.expired_at - current_time
        time_dif_minutes = time_dif.total_seconds() / 60
        sorted_bubbles.append((bubble_algo(time_dif_minutes), bubble))
    
    sorted_bubbles.sort(reverse=True)
    
    print(sorted_bubbles)

    return sorted_bubbles