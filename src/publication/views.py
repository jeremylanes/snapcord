from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from publication.models import PostType, Post, PostMedia, Comment, Reaction


@login_required
def new_post(request):
    user = request.user
    # post_type = PostType.objects.get(name='post')
    if request.method == 'POST' and request.FILES['thumbnail']:
        caption = request.POST.get('caption')
        posttype = request.POST.get('post_type')
        post_type = PostType.objects.get(name=posttype)

        thumbnail = request.FILES['thumbnail']

        post = Post.objects.create(
            user=user,
            type=post_type,
            caption=caption
        )
        PostMedia.objects.create(
            post=post,
            thumbnail=thumbnail
        )
    return redirect('home:index')


@login_required
def comment(request, pk: int):
    if request.method == 'POST':
        user = request.user
        post = Post.objects.get(pk=pk)
        content = request.POST.get('content')
        Comment.objects.create(
            user=user,
            post=post,
            content=content
        )
    return redirect('home:index')


@login_required
def react(request, pk: int):
    user = request.user
    post = Post.objects.get(pk=pk)
    try:
        reaction = Reaction.objects.get(user=user, post=post)
        reaction.delete()
    except:
        Reaction.objects.create(user=user, post=post)

    return redirect('home:index')
