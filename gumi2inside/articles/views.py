from django.shortcuts import render, redirect
from .models import Article
# Create your views here.
def index(request):
    return render(request, "articles/index.html")

def new(request):
    return render(request, 'articles/create.html')

def create(request):
    title = request.POST.get('title')
    content = request.POST.get('content')
    article = Article(title=title,content=content)
    article.save()
    return redirect('articles:index')

def complete(request):
    return render(request, 'articles/complete.html')