from django.core.paginator import Paginator
from django.http import HttpRequest
from django.shortcuts import render, get_object_or_404, redirect

from .models import Post, Comment


def post_list_view(request: HttpRequest):
    post_list = Post.objects.all()
    paginator = Paginator(post_list, 30)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'post_list.html', context={'page_obj': page_obj})


def comments_view(request: HttpRequest, pk: int):
    comment_list = Comment.objects.filter(post_id=pk)
    paginator = Paginator(comment_list, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'comment_list.html', context={
        'page_obj': page_obj,
        'post': Post.objects.get(pk=pk)
    })


def upvote_view(request: HttpRequest, post: int):
    user = request.user
    post = get_object_or_404(Post, pk=post)
    if user.is_authenticated:
        if user in post.upvotes.all():
            post.upvotes.remove(user)
        else:
            post.upvotes.add(user)

    return redirect('post_list')
