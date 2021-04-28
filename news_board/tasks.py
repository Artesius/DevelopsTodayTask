from celery import shared_task

from .models import Post


@shared_task
def clear_votes():
    for post in Post.objects.all():
        post.upvotes.clear()
