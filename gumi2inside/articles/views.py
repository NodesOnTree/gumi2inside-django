from django.shortcuts import render, redirect
from .models import Article, Comment

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

def watch_articles(request):
    article = Article.objects.all()
    comment = Comment.objects.all()

    context={
        'articles' : article,
        'comments' : comment,
    }
    return render(request, "articles/watch_articles.html", context)

def list(request):

    articles = Article.objects.all()
    # index 템플릿에서 사용할 수 있도록 전달
    context = {
        'articles': articles,
    }
    return render(request, 'articles/list.html',context)
