from django.contrib.auth import get_user_model
from django.shortcuts import render
from django.utils import timezone

from publication.models import Post

User = get_user_model()


def index(request):
    posts = Post.objects.all()
    posts = [post for post in posts]
    posts.reverse()
    users = User.objects.all()
    current_date = timezone.now

    context = {
        'users': users,
        'posts': posts,
        'current_date': current_date
    }
    return render(request, 'home/index.html', context=context)
