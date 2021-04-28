from django.contrib.auth.models import User
from django.db import models


class Post(models.Model):
    class Meta:
        db_table = 'post'
        ordering = ['-created']

    title = models.CharField(max_length=100)
    link = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    upvotes = models.ManyToManyField(User, related_name='upvotes', blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def to_dict(self):
        return {
            'id': self.pk,
            'title': self.title,
            'link': self.link,
            'created': self.created,
            'upvotes': self.upvotes.count(),
            'author': self.author.username,
        }


class Comment(models.Model):
    class Meta:
        db_table = 'comment'
        ordering = ['-created']

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def to_dict(self):
        return {
            'id': self.pk,
            'post': self.post.pk,
            'author': self.author.username,
            'content': self.content,
            'created': self.created,
        }
