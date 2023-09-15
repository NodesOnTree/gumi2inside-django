from django.shortcuts import render
from .models import Article, Comment

# Create your views here.
def index(request):
    return render(request, "articles/index.html")

<<<<<<< HEAD

def watch_articles(request):
    article = Article.objects.all()
    comment = Comment.objects.all()

    context={
        'articles' : article,
        'comments' : comment,
    }
    return render(request, "articles/watch_articles.html", context)
=======
def create(request):
    return render(request, "articles/create.html")
>>>>>>> b62371fffe115d444bb9b4fbf3d40cd70ffa4490
def list(request):

    articles = Article.objects.all()
    # index 템플릿에서 사용할 수 있도록 전달
    context = {
        'articles': articles,
    }
    return render(request, 'articles/list.html',context)