from django.shortcuts import render
from .models import Article, Comment

# Create your views here.
def index(request):
    return render(request, "articles/index.html")


def watch_articles(request):
    article = Article.objects.all()
    comment = Comment.objects.all()

    context={
        'articles' : article,
        'comments' : comment,
    }
    return render(request, "articles/watch_articles.html", context)