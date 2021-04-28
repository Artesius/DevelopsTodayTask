from django.urls import path, include

from . import views

urlpatterns = [
    path('', include('news_board.urls')),
    path('api/', include('api.urls')),
    path('account/', include('django.contrib.auth.urls')),
    path('account/register', views.register_view, name='register'),
]
