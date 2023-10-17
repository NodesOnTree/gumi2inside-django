from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import Article, Comment, Poll, Choice, Vote
from common.models import Lunch
from accounts.models import User
from datetime import datetime
from announcements.models import announcement
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from img_upload import img_upload,img_view
from admin_img.models import Carousel
from .forms import PollAddForm, EditPollForm, ChoiceAddForm
from django.core.paginator import Paginator
from django.db.models import Count
from django.contrib import messages
from datetime import datetime
from announcements.models import announcement
from django.utils import timezone

# Create your views here.
def home(request):
    announcements = announcement.objects.order_by('-id')
    announce = ''
    a_menu = Lunch.objects.filter(menuCourseType='AA').order_by('-date').first()
    c_menu = Lunch.objects.filter(menuCourseType='BB').order_by('-date').first()
    
    if announcements.exists():
        for i in announcements:
            announce = i
            break
    carousel1 = Carousel.objects.get(number=1)
    carousel2 = Carousel.objects.get(number=2)
    carousel3 = Carousel.objects.get(number=3)
    context ={
        'announce':announce,
        'a_menu':a_menu,
        'b_menu':c_menu,
        'announce' : announce,
        'carousel1' : carousel1.img_url,
        'carousel2' : carousel2.img_url,
        'carousel3' : carousel3.img_url,
    }    
    return render(request, "articles/home.html", context)



def new(request):
    return render(request, "articles/new.html")


def create(request):
    title = request.POST.get("title")
    content = request.POST.get("content")
    textsize = request.POST.get("textsize")
    red = request.POST.get("red")
    green = request.POST.get("green")
    blue = request.POST.get("blue")
    article = Article(textsize=textsize, red=red, green=green, blue=blue,title=title, content=content, visited_count = 0, like_count = 0, dislike_count = 0)
    article.save()
    if 'file' in request.FILES:
        img_upload(request, article)
    return render(request, "articles/complete.html")


def comment(request, pk):
    content = request.POST.get("comment")
    comment = Comment(content=content, like_count = 0, dislike_count = 0,)
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
        "like" : article.like_count,
        "dislike" : article.dislike_count,
        "textsize" : article.textsize,
        "red" : article.red,
        "green" : article.green,
        "blue" : article.blue,
        "liked_users": article.liked_users.all(),  # 좋아요를 누른 사용자 목록
        "disliked_users": article.disliked_users.all()
    }
    context = img_view(article,context)
    
    return render(request, "articles/detail.html", context)


def articles_list(request):
    articles = Article.objects.order_by('-id')
    months={'01':31, '02':31+28, '03':31+28+31, '04':31+28+31+30, '05':31+28+31+30+31, '06':31+28+31+30+31+30, '07':31+28+31+30+31+30+31, '08':31+28+31+30+31+30+31+31, '09':31+28+31+30+31+30+31+31+30, '10':31+28+31+30+31+30+31+31+30+31, '11':31+28+31+30+31+30+31+31+30+31+30, '12':31+28+31+30+31+30+31+31+30+31+30+31}
    datetime_gaps=[]
    article_titles=[]
    article_pks=[]
    article_contents=[]
    article_like = []
    article_comments = []

    for article in articles:
        time = article.created_at
        comments = article.comment_set.all()
        article_comments.append(len(comments))
        article_titles.append(article.title)
        article_pks.append(article.pk)
        article_like.append(article.like_count)
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


    temp=zip(article_titles,datetime_gaps,article_pks,article_contents, article_like, article_comments)
    context = {
        'temp': temp,
        "articles": articles,
        'datetime_gaps':datetime_gaps,
        "article_titles":article_titles,
        'article_contents':article_contents,
        'article_like': article_like,
        'article_comments': article_comments,
    }
    return render(request, "articles/articles_list.html", context)


@login_required
def delete(request, pk):
    article = Article.objects.get(pk=pk)
    article.delete()
    return redirect("articles:articles_list")


@login_required
def like_article(request, article_pk):
    article = Article.objects.get(pk=article_pk)
    user = request.user

    if user in article.liked_users.all():
        # 이미 좋아요를 누른 경우, 취소 처리
        article.liked_users.remove(user)
        article.like_count -= 1
        article.visited_count -= 1
        article.save()
        return redirect('articles:detail', pk=article.pk)
    
    if user in article.disliked_users.all():
        article.disliked_users.remove(user)
        article.dislike_count -= 1
    # 좋아요 처리
    article.liked_users.add(user)
    article.like_count += 1
    article.visited_count -= 1
    article.save()
    return redirect('articles:detail', pk=article.pk)


@login_required
def dislike_article(request, article_pk):
    article = Article.objects.get(pk=article_pk)
    user = request.user

    if user in article.disliked_users.all():
        # 이미 싫어요를 누른 경우, 취소 처리
        article.disliked_users.remove(user)
        article.dislike_count -= 1
        article.visited_count -= 1
        article.save()
        return redirect('articles:detail', pk=article.pk)
    
    if user in article.liked_users.all():
        article.liked_users.remove(user)
        article.like_count -= 1
    # 싫어요 처리
    article.disliked_users.add(user)
    article.dislike_count += 1
    article.visited_count -= 1
    article.save()
    return redirect('articles:detail', pk=article.pk)


@login_required
def like_comment(request, comment_pk):
    comment = Comment.objects.get(pk=comment_pk)
    comment.origin_article
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
        
    article = comment.origin_article
    article.visited_count -= 1
    article.save()
    comment.save()
    return redirect('articles:detail', pk=article.pk)


@login_required
def dislike_comment(request, comment_pk):
    comment = Comment.objects.get(pk=comment_pk)
    print(comment.origin_article)
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
    article = comment.origin_article
    article.visited_count -= 1
    article.save()
    comment.save()
    return redirect('articles:detail', pk=article.pk)

def polls_list(request):
    all_polls = Poll.objects.order_by('-id')
    paginator = Paginator(all_polls, 10)  # Show 6 contacts per page
    page = request.GET.get('page')
    polls = paginator.get_page(page)

    get_dict_copy = request.GET.copy()
    params = get_dict_copy.pop('page', True) and get_dict_copy.urlencode()
    # current_time = timezone.now()
    # time_difference = current_time - poll.created_at
    context = {
        'polls': polls,
        'params': params,
        
    }
    return render(request, 'articles/polls_list.html', context)


@login_required()
def polls_list_by_user(request):
    all_polls = Poll.objects.filter(owner=request.user)
    paginator = Paginator(all_polls, 10)  # Show 7 contacts per page

    page = request.GET.get('page')
    polls = paginator.get_page(page)

    context = {
        'polls': polls,
    }
    return render(request, 'articles/polls_list.html', context)


@login_required()
def polls_add(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = PollAddForm(request.POST)
            if form.is_valid:
                poll = form.save(commit=False)
                poll.owner = request.user
                poll.save()
                new_choice1 = Choice(
                    poll=poll, choice_text=form.cleaned_data['choice1']).save()
                new_choice2 = Choice(
                    poll=poll, choice_text=form.cleaned_data['choice2']).save()

                
                return redirect('articles:polls_list')
        else:
            form = PollAddForm()
        context = {
            'form': form,
        }
        return render(request, 'articles/add_poll.html', context)
    else:
        return redirect('articles:polls_list')


@login_required
def polls_edit(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    if request.user != poll.owner:
        return redirect('home')

    if request.method == 'POST':
        form = EditPollForm(request.POST, instance=poll)
        if form.is_valid:
            form.save()
            
            return redirect("articles:polls_list")

    else:
        form = EditPollForm(instance=poll)

    return render(request, "articles/poll_edit.html", {'form': form, 'poll': poll})


@login_required
def polls_delete(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    if request.user != poll.owner:
        return redirect('home')
    poll.delete()
    
    return redirect("articles:polls_list")


@login_required
def polls_add_choice(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    if request.user != poll.owner:
        return redirect('home')

    if request.method == 'POST':
        form = ChoiceAddForm(request.POST)
        if form.is_valid:
            new_choice = form.save(commit=False)
            new_choice.poll = poll
            new_choice.save()
            
            return redirect('articles:polls_edit', poll.id)
    else:
        form = ChoiceAddForm()
    context = {
        'form': form,
    }
    return render(request, 'articles/add_choice.html', context)


@login_required
def polls_choice_edit(request, choice_id):
    choice = get_object_or_404(Choice, pk=choice_id)
    poll = get_object_or_404(Poll, pk=choice.poll.id)
    if request.user != poll.owner:
        return redirect('home')

    if request.method == 'POST':
        form = ChoiceAddForm(request.POST, instance=choice)
        if form.is_valid:
            new_choice = form.save(commit=False)
            new_choice.poll = poll
            new_choice.save()

            return redirect('articles:polls_edit', poll.id)
    else:
        form = ChoiceAddForm(instance=choice)
    context = {
        'form': form,
        'edit_choice': True,
        'choice': choice,
    }
    return render(request, 'articles/polls_add_choice.html', context)


@login_required
def polls_choice_delete(request, choice_id):
    choice = get_object_or_404(Choice, pk=choice_id)
    poll = get_object_or_404(Poll, pk=choice.poll.id)
    if request.user != poll.owner:
        return redirect('home')
    choice.delete()

    return redirect('articles:polls_edit', poll.id)


def poll_detail(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id)

    if not poll.active:
        return render(request, 'articles/poll_result.html', {'poll': poll})
    loop_count = poll.choice_set.count()
    context = {
        'poll': poll,
        'loop_time': range(0, loop_count),
    }
    return render(request, 'articles/poll_detail.html', context)


@login_required
def poll_vote(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    choice_id = request.POST.get('choice')
    user_can_vote = poll.user_can_vote(request.user)
    choice = Choice.objects.get(id=choice_id)
    user=request.user
    if not poll.user_can_vote(request.user):
        vote = Vote.objects.get(poll_id=poll_id,user_id=user.id)
        
        vote.choice=choice
        vote.save()
        context={
            'poll': poll,
            'user_can_vote' : user_can_vote
        }
        return render(request, 'articles/poll_result.html',context )

    if choice_id:
        
        vote = Vote(user=request.user, poll=poll, choice=choice)
        vote.save()
        context={
            'poll': poll,
            'user_can_vote' : user_can_vote
        }
        return render(request, 'articles/poll_result.html',context )
    else:

        return redirect("articles:polls_detail", poll_id)
    


@login_required
def polls_endpoll(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    if request.user != poll.owner:
        return redirect('home')

    if poll.active is True:
        poll.active = False
        poll.save()
        return render(request, 'articles/poll_result.html', {'poll': poll})
    else:
        return render(request, 'articles/poll_result.html', {'poll': poll})
