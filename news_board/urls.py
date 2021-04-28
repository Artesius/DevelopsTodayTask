from django.urls import path

from . import views

urlpatterns = [
    path('', views.post_list_view, name='post_list'),
    path('<int:pk>', views.comments_view, name='comment_list'),
    path('upvote/<int:post>', views.upvote_view, name='upvote'),
]
