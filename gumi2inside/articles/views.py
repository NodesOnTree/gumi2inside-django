from django.shortcuts import render, redirect
from .models import Article, Comment


# Create your views here.
def home(request):
    return render(request, "articles/home.html")


def new(request):
    return render(request, "articles/new.html")


def create(request):
    title = request.POST.get("title")
    content = request.POST.get("content")
    article = Article(title=title, content=content)
    article.save()
    return render(request, "articles/complete.html")


def complete(request):
    return redirect("articles:list")


def detail(request, pk):
    article = Article.objects.get(pk=pk)
    context = {
        "pk": pk,
        "title": article.title,
        "content": article.content,
    }
    return render(request, "articles/detail.html", context)


def list(request):
    articles = Article.objects.all()
    context = {
        "articles": articles,
    }
    return render(request, "articles/list.html", context)


# def delete(request):
#     articles = Aricle.


def delete(request, pk):
    article = Article.objects.get(pk=pk)
    article.delete()
    return redirect("articles:list")
