from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.handlers.wsgi import WSGIRequest


@login_required
def users(request: WSGIRequest):
    return render(request, 'administration/users.html', {
        'count': [i for i in range(10)]
    })
