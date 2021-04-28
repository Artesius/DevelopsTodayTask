from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token

from . import views

urlpatterns = [
    path('api-token-auth/', obtain_jwt_token),
    path('publications', views.post_view, name='post'),
    path('comments', views.comment_view, name='comment'),
    path('upvote', views.upvote_view, name='upvote_post'),
]
