from django.shortcuts import render, redirect
from django.urls import reverse
from img_upload import img_upload,img_view
from .models import Rboard, Comment
from datetime import datetime
from django.contrib.auth.decorators import login_required


@login_required
def new(request):
    return render(request, "rboards/new.html")


@login_required
def create(request):
    # print(request.user.first_name)
    title = request.POST.get("title")
    content = request.POST.get("content")
    textsize = request.POST.get("textsize")
    red = request.POST.get("red")
    green = request.POST.get("green")
    blue = request.POST.get("blue")
    # print(red,green,blue)
    rboard = Rboard(textsize=textsize, red=red, green=green, blue=blue,title=title, content=content, visited_count = 0,author=request.user)
    rboard.save()
    if 'file' in request.FILES:
        print('왔다!!')
        img_upload(request, rboard)
    return render(request, "rboards/complete.html")


@login_required
def comment(request, pk):
    content = request.POST.get("comment")
    comment = Comment(content=content)
    comment.origin_rboard = Rboard.objects.get(pk=pk)
    comment.user = request.user
    comment.save()
    return redirect(reverse('rboards:detail', kwargs={'pk': pk}))


@login_required
def complete(request):
    return redirect("rboards:rboards_list")


def detail(request, pk):
    rboard = Rboard.objects.get(pk=pk)
    time = rboard.created_at
    new_datetime=''
    new_datetime+=str(time)[0:11]
    new_datetime+=str(time)[11:16]
    comments = rboard.comment_set.all()
    rboard.visited_count += 1
    rboard.save()
    user = rboard.author
    author = user.first_name
    user_pk = user.pk
    
    context = {
        "rborad" : rboard,
        "pk": pk,
        "title": rboard.title,
        "content": rboard.content,
        "new_datetime": new_datetime,
        "comments": comments,
        "comments_count": len(comments),
        "visited_count": rboard.visited_count,
        "textsize" : rboard.textsize,
        "red" : rboard.red,
        "green" : rboard.green,
        "blue" : rboard.blue,
        "author" : author,
        "like" : rboard.like_count,
        "dislike" : rboard.dislike_count,
        'user_pk':user_pk,
        "liked_users": rboard.liked_users.all(),  # 좋아요를 누른 사용자 목록
        "disliked_users": rboard.disliked_users.all()
    }
    context = img_view(rboard,context)
    return render(request, "rboards/detail.html", context)


def rboards_list(request):
    rboards = Rboard.objects.order_by('-id')
    context = {
     'rboards' : rboards,
    }
    return render(request, "rboards/rboards_list.html", context)


@login_required
def delete(request, pk):
    rboard = Rboard.objects.get(pk=pk)
    rboard.delete()
    return redirect("rboards:rboards_list")


@login_required
def like_article(request, article_pk):
    rboard = Rboard.objects.get(pk=article_pk)
    user = request.user

    if user in rboard.liked_users.all():
        # 이미 좋아요를 누른 경우, 취소 처리
        rboard.liked_users.remove(user)
        rboard.like_count -= 1
        rboard.visited_count -= 1
        rboard.save()
        return redirect('rboards:detail', pk=rboard.pk)
    
    if user in rboard.disliked_users.all():
        rboard.disliked_users.remove(user)
        rboard.dislike_count -= 1
    # 좋아요 처리
    rboard.liked_users.add(user)
    rboard.like_count += 1
    rboard.visited_count -= 1
    rboard.save()
    return redirect('rboards:detail', pk=rboard.pk)


@login_required
def dislike_article(request, article_pk):
    rboard = Rboard.objects.get(pk=article_pk)
    user = request.user

    if user in rboard.disliked_users.all():
        # 이미 싫어요를 누른 경우, 취소 처리
        rboard.disliked_users.remove(user)
        rboard.dislike_count -= 1
        rboard.visited_count -= 1
        rboard.save()
        return redirect('rboards:detail', pk=rboard.pk)
    
    if user in rboard.liked_users.all():
        rboard.liked_users.remove(user)
        rboard.like_count -= 1
    # 싫어요 처리
    rboard.disliked_users.add(user)
    rboard.dislike_count += 1
    rboard.visited_count -= 1
    rboard.save()
    return redirect('rboards:detail', pk=rboard.pk)


@login_required
def like_comment(request, comment_pk):
    comment = Comment.objects.get(pk=comment_pk)
    user = request.user

    if user in comment.comment_liked_users.all():
        # 이미 좋아요를 누른 경우, 취소 처리
        comment.comment_liked_users.remove(user)
        comment.like_count -= 1
    else:
        if user in comment.comment_disliked_users.all():
            comment.comment_disliked_users.remove(user)
            comment.dislike_count -= 1
        # 좋아요 처리
        comment.comment_liked_users.add(user)
        comment.like_count += 1
        
    rboard = comment.origin_rboard
    rboard.visited_count -= 1
    rboard.save()
    comment.save()
    return redirect('rboards:detail', pk=rboard.pk)


@login_required
def dislike_comment(request, comment_pk):
    comment = Comment.objects.get(pk=comment_pk)
    user = request.user

    if user in comment.comment_disliked_users.all():
        # 이미 싫어요를 누른 경우, 취소 처리
        comment.comment_disliked_users.remove(user)
        comment.dislike_count -= 1
    else:
    
        if user in comment.comment_liked_users.all():
            comment.comment_liked_users.remove(user)
            comment.like_count -= 1
        # 싫어요 처리
        comment.comment_disliked_users.add(user)
        comment.dislike_count += 1
    rboard = comment.origin_rboard
    rboard.visited_count -= 1
    rboard.save()
    comment.save()
    return redirect('rboards:detail', pk=rboard.pk)