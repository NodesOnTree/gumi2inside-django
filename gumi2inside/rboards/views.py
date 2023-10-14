from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Rboard, Comment
from datetime import datetime
from announcements.models import announcement
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):
    announcements = announcement.objects.order_by('-id')
    announce = ''
    # print(a)
    if announcements.exists():
        for i in announcements:
            announce = i
            break
    context ={
        'announce':announce
    }    
    return render(request, "rboards/home.html", context)

@login_required
def new(request):
    return render(request, "rboards/new.html")

@login_required
def create(request):
    title = request.POST.get("title")
    content = request.POST.get("content")
    textsize = request.POST.get("textsize")
    red = request.POST.get("red")
    green = request.POST.get("green")
    blue = request.POST.get("blue")
    print(red,green,blue)
    rboard = Rboard(textsize=textsize, red=red, green=green, blue=blue,title=title, content=content, visited_count = 0)
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
    context = {
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
    }
    
    return render(request, "rboards/detail.html", context)


def rboards_list(request):
    rboards = Rboard.objects.order_by('-id')
    months={'01':31, '02':31+28, '03':31+28+31, '04':31+28+31+30, '05':31+28+31+30+31, '06':31+28+31+30+31+30, '07':31+28+31+30+31+30+31, '08':31+28+31+30+31+30+31+31, '09':31+28+31+30+31+30+31+31+30, '10':31+28+31+30+31+30+31+31+30+31, '11':31+28+31+30+31+30+31+31+30+31+30, '12':31+28+31+30+31+30+31+31+30+31+30+31}
    datetime_gaps=[]
    rboard_titles=[]
    rboard_pks=[]
    rboard_contents=[]

    for rboard in rboards:
        time = rboard.created_at
        rboard_titles.append(rboard.title)
        rboard_pks.append(rboard.pk)
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


    temp=zip(rboard_titles,datetime_gaps,rboard_pks,rboard_contents)
    context = {
        'temp': temp,
        "rboards": rboards,
        'datetime_gaps':datetime_gaps,
        "rboard_titles":rboard_titles,
        'rboard_contents':rboard_contents,

    }
    return render(request, "rboards/rboards_list.html", context)

    rboards = Rboard.objects.order_by('-id')
    months={'01':31, '02':31+28, '03':31+28+31, '04':31+28+31+30, '05':31+28+31+30+31, '06':31+28+31+30+31+30, '07':31+28+31+30+31+30+31, '08':31+28+31+30+31+30+31+31, '09':31+28+31+30+31+30+31+31+30, '10':31+28+31+30+31+30+31+31+30+31, '11':31+28+31+30+31+30+31+31+30+31+30, '12':31+28+31+30+31+30+31+31+30+31+30+31}
    datetime_gaps=[]
    rboard_titles=[]
    rboard_pks=[]
    rboard_contents=[]

    for rboard in rboards:
        time = rboard.created_at
        rboard_titles.append(rboard.title)
        rboard_pks.append(rboard.pk)
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


    temp=zip(rboard_titles,datetime_gaps,rboard_pks,rboard_contents)
    context = {
        'temp': temp,
        "rboards": rboards,
        'datetime_gaps':datetime_gaps,
        "rboard_titles":rboard_titles,
        'rboard_contents':rboard_contents,

    }
    return render(request, "rboards/announcement.html", context)



@login_required
def delete(request, pk):
    rboard = Rboard.objects.get(pk=pk)
    rboard.delete()
    return redirect("rboards:rboards_list")
