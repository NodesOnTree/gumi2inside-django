from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Rboard, Comment
from datetime import datetime
from announcements.models import announcement
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
    return render(request, "rboards/complete.html")


@login_required
def comment(request, pk):
    content = request.POST.get("comment")
    comment = Comment(content=content)
    comment.origin_rboard = Rboard.objects.get(pk=pk)
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
    print(context)
    return render(request, "rboards/detail.html", context)


def rboards_list(request):
    rboards = Rboard.objects.order_by('-id')
    months={'01':31, '02':31+28, '03':31+28+31, '04':31+28+31+30, '05':31+28+31+30+31, '06':31+28+31+30+31+30, '07':31+28+31+30+31+30+31, '08':31+28+31+30+31+30+31+31, '09':31+28+31+30+31+30+31+31+30, '10':31+28+31+30+31+30+31+31+30+31, '11':31+28+31+30+31+30+31+31+30+31+30, '12':31+28+31+30+31+30+31+31+30+31+30+31}
    datetime_gaps=[]
    rboard_titles=[]
    rboard_pks=[]
    rboard_contents=[]
    rboard_name = []
    rboard_like = []
    rboard_comments = []
    
    for rboard in rboards:
        time = rboard.created_at
        comments = rboard.comment_set.all()
        rboard_comments.append(len(comments))
        rboard_titles.append(rboard.title)
        rboard_pks.append(rboard.pk)
        rboard_name.append(rboard.author.first_name)
        rboard_like.append(rboard.like_count)
        if len(rboard.content)>=40:
            content=rboard.content[0:40]
            content+='...'
            rboard_contents.append(content)
        else:
            rboard_contents.append(rboard.content)
        new_datetime=''
        new_datetime+=str(time)[0:11]
        new_datetime+=str(time)[11:16]

        current_time = datetime.now()
        now_datetime=''
        now_datetime+=str(current_time)[0:11]
        now_datetime+=str(current_time)[11:16]
       
        now_date=int(str(current_time)[0:11].replace('-',''))
        now_year=str(now_date)[0:4]
        now_month=str(now_date)[4:6]
        now_day=str(now_date)[6:]
        write_date=int(str(time)[0:11].replace('-',''))
        write_year=str(write_date)[0:4]
        write_month=str(write_date)[4:6]
        write_day=str(write_date)[6:]
        new_time=int(str(time)[11:13])*60+int(str(time)[14:16])
    
        now_time=int(str(current_time)[11:13])*60+int(str(current_time)[14:16])
       
        time_gap=now_time-new_time
        
        if now_date-write_date>=1:
            nowdays= int(now_day)+months[now_month]
            writedays= int(write_day)+months[write_month]
            if now_year!=write_year:
                nowdays+=365*(int(now_year)-int(write_year))
                if nowdays-writedays>=365:
                    datetime_gaps.append(f'{int(now_year)-int(write_year)}년 전')
                elif nowdays-writedays<365:
                    datetime_gaps.append(f'{nowdays-writedays}일 전')
            else:
                datetime_gaps.append(f'{nowdays-writedays}일 전')
        else:
            if time_gap>=60:
                datetime_gaps.append(f'{time_gap//60}시간 전')
            else:
                datetime_gaps.append(f'{time_gap}분 전')

    # rboard = Rboard.objects.get(pk=pk)
    # user = rboard.author
    # author = rboard.user
    temp=zip(rboard_titles,datetime_gaps,rboard_pks,rboard_contents, rboard_name, rboard_like, rboard_comments)
    context = {
        'temp': temp,
        "rboards": rboards,
        'datetime_gaps':datetime_gaps,
        "rboard_titles":rboard_titles,
        'rboard_contents':rboard_contents,
        'rboard_name': rboard_name,
        'rboard_like': rboard_like,
        'rboard_comments': rboard_comments,
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