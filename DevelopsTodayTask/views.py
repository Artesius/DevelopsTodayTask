from django.contrib.auth.models import User
from django.shortcuts import render


def register_view(request):
    if request.method == 'GET':
        return render(request, 'registration/registration.html')
    elif request.method == 'POST':
        login = request.POST.get('login', None)
        password = request.POST.get('password', None)
        if not login or not password:
            return render(
                request,
                'registration/registration.html',
                context={'context': 'All the fields should be filled'},
            )
        User.objects.create_user(username=login, password=password).save()
        return render(
            request,
            'registration/registration.html',
            context={'context': 'Successfully registered'},
        )