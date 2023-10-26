from django import template
from django.utils import timezone
from datetime import timedelta

register = template.Library()
app_name = 'my_custom_filters'
@register.filter
def time_difference_with_now(created_at):
    now = timezone.now()
    time_difference = now - created_at
    days = time_difference.days
    seconds = time_difference.seconds
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    if days > 0:
        return f"{days}일 전"
    elif hours > 0:
        return f"{hours}시간 전"
    elif minutes > 0:
        return f"{minutes}분 전"
    else:
        return "방금 전"