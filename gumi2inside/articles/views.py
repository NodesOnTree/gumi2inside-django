from django.shortcuts import render, redirect
from .models import Article, Comment

# Create your views here.
def home(request):
    return render(request, "articles/home.html")

def create(request):
    # title = request.POST.get('title')
    # content = request.POST.get('content')
    # article = Article(title=title, content=content)
    # article.save()
    return render(request, 'articles/create.html')

def watch_articles(request):
    title = request.POST.get('title')
    content = request.POST.get('content')
    article = Article(title=title, content=content)
    article.save()
    articles = Article.objects.all()
    comments = Comment.objects.all()

    context = {
        'articles': articles,
        'comments': comments,
    }
    return render(request, "articles/watch_articles.html", context)

def list(request):
    articles = Article.objects.all()
    context = {
        'articles': articles,
    }
    return render(request, 'articles/list.html', context)
