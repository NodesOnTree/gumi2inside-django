from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Article, Comment
from datetime import datetime

# Create your views here.
def home(request):
    return render(request, "articles/home.html")


def new(request):
    return render(request, "articles/new.html")


def create(request):
    title = request.POST.get("title")
    content = request.POST.get("content")
    textsize = request.POST.get("textsize")
    red = request.POST.get("red")
    green = request.POST.get("green")
    blue = request.POST.get("blue")
    print(red,green,blue)
    article = Article(textsize=textsize, red=red, green=green, blue=blue,title=title, content=content, visited_count = 0)
    article.save()
    return render(request, "articles/complete.html")

def comment(request, pk):
    content = request.POST.get("comment")
    comment = Comment(content=content)
    comment.origin_article = Article.objects.get(pk=pk)
    comment.save()
    return redirect(reverse('articles:detail', kwargs={'pk': pk}))

def complete(request):
    return redirect("articles:articles_list")


def detail(request, pk):
    article = Article.objects.get(pk=pk)
    time = article.created_at
    new_datetime=''
    new_datetime+=str(time)[0:11]
    new_datetime+=str(time)[11:16]
    comments = article.comment_set.all()
    article.visited_count += 1
    article.save()
    context = {
        "pk": pk,
        "title": article.title,
        "content": article.content,
        "new_datetime": new_datetime,
        "comments": comments,
        "comments_count": len(comments),
        "visited_count": article.visited_count,
        "textsize" : article.textsize,
        "red" : article.red,
        "green" : article.green,
        "blue" : article.blue,
    }
    
    return render(request, "articles/detail.html", context)


def articles_list(request):
    articles = Article.objects.order_by('-id')
   
    datetime_gaps=[]
    article_titles=[]
    article_pks=[]
    article_contents=[]

    for article in articles:
        time = article.created_at
        article_titles.append(article.title)
        article_pks.append(article.pk)
        if len(article.content)>=40:
            content=article.content[0:40]
            content+='...'
            article_contents.append(content)
        else:
            article_contents.append(article.content)
        new_datetime=''
        new_datetime+=str(time)[0:11]
        new_datetime+=str(time)[11:16]

        current_time = datetime.now()
        now_datetime=''
        now_datetime+=str(current_time)[0:11]
        now_datetime+=str(current_time)[11:16]
       
        now_date=int(str(current_time)[0:11].replace('-',''))
       
        write_date=int(str(time)[0:11].replace('-',''))
      
        new_time=int(str(time)[11:13])*60+int(str(time)[14:16])
    
        now_time=int(str(current_time)[11:13])*60+int(str(current_time)[14:16])

        time_gap=now_time-new_time
        
        if now_date-write_date>=1:
            date_gap=now_date-write_date
            datetime_gaps.append(f'{date_gap}일 전')
        else:
            if time_gap>=60:
                datetime_gaps.append(f'{time_gap//60}시간 전')
            else:
                datetime_gaps.append(f'{time_gap}분 전')

    temp=zip(article_titles,datetime_gaps,article_pks,article_contents)
    context = {
        'temp': temp,
        "articles": articles,
        'datetime_gaps':datetime_gaps,
        "article_titles":article_titles,
        'article_contents':article_contents,

    }
    return render(request, "articles/articles_list.html", context)




def delete(request, pk):
    article = Article.objects.get(pk=pk)
    article.delete()
    return redirect("articles:articles_list")
