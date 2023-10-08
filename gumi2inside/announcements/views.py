from django.shortcuts import render, redirect
from django.urls import reverse
from datetime import datetime
from articles.models import Article
from .models import announcement
# 공지사항
def announcement_list(request):
    announces=announcement.objects.all()
    context={
        'announces':announces
    }
    return render(request, "announcements/announcement.html", context)
