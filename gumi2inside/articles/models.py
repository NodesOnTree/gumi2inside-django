from django.db import models
from django.conf import settings
from accounts.models import User
from django.utils import timezone
import secrets

# Create your models here.
class Article(models.Model):
    title = models.CharField(max_length=30)
    content = models.TextField()
    textsize = models.TextField()
    red = models.TextField()
    green = models.TextField()
    blue = models.TextField()
    image = models.ImageField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    visited_count = models.IntegerField()
    like_count = models.IntegerField(default=0)
    dislike_count = models.IntegerField(default=0)
    liked_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="liked_articles")
    disliked_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="disliked_articles")
    img_url = models.TextField()
    status = models.TextField(default="Article")

class Comment(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    origin_article = models.ForeignKey('Article', on_delete=models.CASCADE)
    like_count = models.IntegerField(default=0)
    dislike_count = models.IntegerField(default=0)
    comment_liked_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="liked_comments")
    comment_disliked_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="disliked_comments")


class Poll(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=30)
    text = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)  # created_at 필드에 현재 시간을 저장
    active = models.BooleanField(default=True)

    def user_can_vote(self, user):
        """ 
        Return False if user already voted
        """
        user_votes = user.vote_set.all()
        qs = user_votes.filter(poll=self)
        if qs.exists():
            return False
        return True

    @property
    def get_vote_count(self):
        return self.vote_set.count()

    def get_result_dict(self):
        res = []
        for choice in self.choice_set.all():
            d = {}
            alert_class = ['primary', 'secondary', 'success',
                           'danger', 'dark', 'warning', 'info']

            d['alert_class'] = secrets.choice(alert_class)
            d['text'] = choice.choice_text
            d['num_votes'] = choice.get_vote_count
            if not self.get_vote_count:
                d['percentage'] = 0
            else:
                d['percentage'] = (choice.get_vote_count /
                                   self.get_vote_count)*100

            res.append(d)
        return res

    def __str__(self):
        return self.text


class Choice(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=255)

    @property
    def get_vote_count(self):
        return self.vote_set.count()

    def __str__(self):
        return f"{self.poll.text[:25]} - {self.choice_text[:25]}"


class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.poll.text[:15]} - {self.choice.choice_text[:15]} - {self.user.username}'
